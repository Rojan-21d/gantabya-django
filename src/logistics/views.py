# logistics/views.py

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from logistics.utils import BookingStatus, LoadStatus, pricing_options
from .models import Load, Booking, PricingAlgorithm

from .models import Load, Booking
from .forms import LoadForm
from .mixins import ConsignorRequiredMixin, CarrierRequiredMixin

# --- Views for Consignors ---

class MyLoadsListView(LoginRequiredMixin, ConsignorRequiredMixin, ListView):
    """
    Displays a list of loads created by the currently logged-in consignor.
    """
    model = Load
    template_name = 'logistics/my_loads.html'
    context_object_name = 'loads'

    def get_queryset(self):
        return Load.objects.filter(consignor=self.request.user).order_by('-created_at')

class LoadCreateView(LoginRequiredMixin, ConsignorRequiredMixin, CreateView):
    """
    Allows a consignor to create a new load.
    """
    model = Load
    form_class = LoadForm
    template_name = 'logistics/load_form.html'
    success_url = reverse_lazy('my_loads') # Redirect to their list of loads

    def form_valid(self, form):
        form.instance.consignor = self.request.user
        messages.success(self.request, "Load created successfully! Carriers can now view it.")
        return super().form_valid(form)

# --- Views for Carriers ---

class AvailableLoadsListView(LoginRequiredMixin, CarrierRequiredMixin, ListView):
    """
    Displays all available loads (status='PENDING') for carriers to book.
    """
    model = Load
    template_name = 'logistics/available_loads.html'
    context_object_name = 'loads'
    
    def get_queryset(self):
        return Load.objects.filter(status=LoadStatus.PENDING).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_loads = self.get_queryset()
        active_count = active_loads.count()
        load_cards = []
        for load in active_loads:
            load_cards.append({
                "load": load,
                "prices": pricing_options(load, self.request.user, active_count)
            })
        context["load_cards"] = load_cards
        return context

class LoadDetailView(LoginRequiredMixin, DetailView):
    """
    Shows details for a single load. Accessible by both user types.
    """
    model = Load
    template_name = 'logistics/load_detail.html'
    context_object_name = 'load'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        load = self.get_object()
        if getattr(self.request.user, "user_type", None) == "carrier":
            active_count = Load.objects.filter(status=LoadStatus.PENDING).count()
            context["price_options"] = pricing_options(load, self.request.user, active_count)
        return context


class BookLoadView(LoginRequiredMixin, CarrierRequiredMixin, View):
    """
    Handles the logic for a carrier to book a load.
    """
    def post(self, request, *args, **kwargs):
        load_id = self.kwargs.get('pk')
        load = get_object_or_404(Load, id=load_id)
        selected_algo = request.POST.get("algorithm", PricingAlgorithm.DYNAMIC)

        if load.status != LoadStatus.PENDING:
            messages.error(request, "This load is no longer available.")
            return redirect('available_loads')

        # Prevent duplicate booking attempts
        if hasattr(load, "booking"):
            messages.error(request, "This load has already been booked.")
            return redirect('available_loads')

        active_count = Load.objects.filter(status=LoadStatus.PENDING).count()
        price_data = pricing_options(load, request.user, active_count).get(selected_algo)
        if not price_data or price_data.get("price") is None:
            messages.error(request, "Unable to calculate price for the selected algorithm.")
            return redirect('available_loads')

        try:
            # Use a transaction to ensure both operations succeed or fail together
            with transaction.atomic():
                Booking.objects.create(
                    load=load,
                    carrier=request.user,
                    selected_algorithm=selected_algo,
                    price=price_data.get("price"),
                    distance_km=price_data.get("distance_km"),
                )
                # Update the load status
                load.status = LoadStatus.BOOKED
                load.save()
            
            messages.success(
                request,
                f"You have successfully booked the load: {load.name} "
                f"using {PricingAlgorithm(selected_algo).label} for NPR {price_data.get('price')}.",
            )
        except Exception as e:
            messages.error(request, f"An error occurred while booking. Please try again. Error: {e}")
        
        return redirect('my_bookings')


class MyBookingsListView(LoginRequiredMixin, CarrierRequiredMixin, ListView):
    """
    Displays all loads booked by the currently logged-in carrier.
    """
    model = Booking
    template_name = 'logistics/my_bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(carrier=self.request.user).select_related('load').order_by('-booked_at')
