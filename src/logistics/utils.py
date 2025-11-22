from django.db import models

class LoadStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    BOOKED = 'BOOKED', 'Booked'
    IN_TRANSIT = 'IN_TRANSIT', 'In Transit'
    COMPLETED = 'COMPLETED', 'Completed'
    CANCELLED = 'CANCELLED', 'Cancelled'
    

class BookingStatus(models.TextChoices):
    CONFIRMED = 'CONFIRMED', 'Confirmed'
    CANCELLED = 'CANCELLED', 'Cancelled'


# --- Pricing helpers ---------------------------------------------------------
# These helpers stay in utils so they can be reused by views, forms, and admin.

from math import radians, sin, cos, sqrt, atan2
from datetime import date


def haversine_distance_km(lat1, lon1, lat2, lon2):
    """
    Compute haversine distance in KM between two coordinate pairs.
    Returns None when any coordinate is missing.
    """
    if None in (lat1, lon1, lat2, lon2):
        return None

    rlat1, rlon1, rlat2, rlon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = rlon2 - rlon1
    dlat = rlat2 - rlat1
    a = sin(dlat / 2) ** 2 + cos(rlat1) * cos(rlat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    earth_radius_km = 6371
    return round(earth_radius_km * c, 2)


def dynamic_pricing(load, carrier, active_loads_count=0):
    """
    Dynamic pricing that considers base cost + load weight + market surge.
    - More active loads => higher surge
    - Loads scheduled soon => slight surge
    """
    base_fee = 200  # flat booking support fee
    weight_component = float(load.weight) * 5  # NPR per kg (example)

    surge_from_demand = 1 + min(active_loads_count / 20, 0.5)  # cap at +50%

    days_until = (load.scheduled_date - date.today()).days if load.scheduled_date else 0
    urgency_factor = 1.0
    if days_until <= 1:
        urgency_factor = 1.3
    elif days_until <= 3:
        urgency_factor = 1.15

    price = (base_fee + weight_component) * surge_from_demand * urgency_factor
    return round(price, 2)


def location_pricing(load, carrier, default_rate_per_km=90):
    """
    Location/distance pricing using haversine distance and carrier's rate.
    """
    distance_km = haversine_distance_km(
        load.pickup_latitude,
        load.pickup_longitude,
        load.destination_latitude,
        load.destination_longitude,
    )
    if distance_km is None:
        return None, None

    rate = float(getattr(carrier, "base_rate_per_km", None) or default_rate_per_km)
    base_weight_component = float(load.weight) * 3
    price = distance_km * rate + base_weight_component
    return round(price, 2), distance_km


def weight_class_pricing(load, carrier):
    """
    Pricing that respects carrier vehicle capacity.
    - Under capacity: cheaper multiplier
    - Over capacity: penalty multiplier
    """
    capacity = float(getattr(carrier, "vehicle_capacity_kg", 0) or 0)
    weight = float(load.weight)

    if capacity <= 0:
        multiplier = 1.25  # unknown capacity: slight penalty
    elif weight <= capacity:
        multiplier = 0.9  # reward right-fit loads
    else:
        multiplier = 1.4  # penalty for overweight relative to capacity

    base = 150 + weight * 6
    return round(base * multiplier, 2)


def pricing_options(load, carrier, active_loads_count=0):
    """
    Return a dictionary of pricing strategies for easy rendering.
    """
    dynamic_price = dynamic_pricing(load, carrier, active_loads_count)
    distance_price, distance_km = location_pricing(load, carrier)
    weight_price = weight_class_pricing(load, carrier)

    return {
        "dynamic": {"label": "Dynamic (market + urgency)", "price": dynamic_price},
        "distance": {
            "label": "Location (haversine)",
            "price": distance_price,
            "distance_km": distance_km,
        },
        "weight": {
            "label": "Vehicle Weight Fit",
            "price": weight_price,
            "capacity": getattr(carrier, "vehicle_capacity_kg", None),
        },
    }
