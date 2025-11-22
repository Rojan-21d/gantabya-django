from django.contrib import admin
from .models import Load, Booking


@admin.register(Load)
class LoadAdmin(admin.ModelAdmin):
    list_display = ("name", "consignor", "weight", "status", "scheduled_date")
    list_filter = ("status", "scheduled_date")
    search_fields = ("name", "pickup_address", "destination_address")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("load", "carrier", "selected_algorithm", "price", "status", "booked_at")
    list_filter = ("selected_algorithm", "status")
    search_fields = ("load__name", "carrier__email")
