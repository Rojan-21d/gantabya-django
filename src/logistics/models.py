from django.db import models
from django.conf import settings

from logistics.utils import BookingStatus, LoadStatus
from user_management.models import TimeStamp, UserStamp 


class PricingAlgorithm(models.TextChoices):
    DYNAMIC = "dynamic", "Dynamic (market/urgency)"
    DISTANCE = "distance", "Location (haversine)"
    WEIGHT = "weight", "Vehicle weight fit"

class Load(UserStamp, TimeStamp):
    """
    Represents a load posted by a Consignor.
    """
    consignor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='loads',
        limit_choices_to={'user_type': 'consignor'},
    )
    name = models.CharField(
        max_length=255, 
        help_text="e.g., 'Electronics from Kathmandu to Pokhara'"
    )
    description = models.TextField()
    pickup_address = models.CharField(
        max_length=255
    )
    pickup_latitude = models.FloatField(null=True, blank=True)
    pickup_longitude = models.FloatField(null=True, blank=True)
    destination_address = models.CharField(
        max_length=255
    )
    destination_latitude = models.FloatField(null=True, blank=True)
    destination_longitude = models.FloatField(null=True, blank=True)
    weight = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Weight in kilograms"
    )
    scheduled_date = models.DateField()
    status = models.CharField(
        max_length=20, 
        choices=LoadStatus.choices, 
        default=LoadStatus.PENDING
    )

    def __str__(self):
        return f"{self.name} by {self.consignor.username}"

class Booking(UserStamp, TimeStamp):
    """
    Represents a booking made by a Carrier for a specific Load.
    """

    # Using OneToOneField ensures one load can only be booked once.
    load = models.OneToOneField(Load, on_delete=models.CASCADE, related_name='booking')
    carrier = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
        limit_choices_to={'user_type': 'carrier'},
    )
    status = models.CharField(max_length=20, choices=BookingStatus.choices, default=BookingStatus.CONFIRMED)
    selected_algorithm = models.CharField(
        max_length=20,
        choices=PricingAlgorithm.choices,
        default=PricingAlgorithm.DYNAMIC,
    )
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    distance_km = models.FloatField(null=True, blank=True)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        suffix = f" @ {self.price}" if self.price else ""
        return f"Booking for '{self.load.name}' by {self.carrier.username}{suffix}"
