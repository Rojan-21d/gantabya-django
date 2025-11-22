from django.views import View
from django.views.generic import FormView
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.urls import reverse_lazy
from .forms import LoginForm
from django.views.generic.edit import CreateView
from .forms import RegisterForm
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .models import CustomUser
from .forms import ProfileUpdateForm
User = get_user_model()
from django.contrib.auth.views import LogoutView

class RegisterView(CreateView):
    model = CustomUser
    form_class = RegisterForm
    template_name = "register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, "Registration successful! Please log in.")
        return super().form_valid(form)

class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = reverse_lazy("home")
    
    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user_type = form.cleaned_data['user_type']

        # Attempt to authenticate the user
        user = authenticate(self.request, email=email, password=password)

        if user is not None:
            if hasattr(user, 'user_type') and user.user_type == user_type:
                login(self.request, user)
                return super().form_valid(form)
            else:
                form.add_error(None, "User type mismatch.")
        else:
            form.add_error(None, "Invalid email or password.")
        
        return self.form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)
    

class HomeView(LoginRequiredMixin, View):
    login_url = 'login'  # your login URL name

    def get(self, request, *args, **kwargs):
        user = request.user

        # Route users directly to their primary dashboard
        if getattr(user, "user_type", None) == "carrier":
            return redirect("available_loads")
        if getattr(user, "user_type", None) == "consignor":
            return redirect("my_loads")
        return render(request, 'main/base.html', {"user_type": getattr(user, "user_type", 'unknown')})

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = "profile.html"
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = form.save(commit=False)
        new_password = form.cleaned_data.get('password')

        if new_password:
            user.set_password(new_password)
        user.save()

        # Must come after user.save()
        if new_password:
            update_session_auth_hash(self.request, user)

        messages.success(self.request, "Profile updated successfully!")
        return redirect(self.success_url)  # avoid super().form_valid to prevent re-saving

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

    
class CustomLogoutView(LogoutView):
    next_page = 'login'

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have successfully logged out.")
        return super().dispatch(request, *args, **kwargs)
