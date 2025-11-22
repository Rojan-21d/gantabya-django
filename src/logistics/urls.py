from django.urls import path
from .views import (
    MyLoadsListView,
    LoadCreateView,
    AvailableLoadsListView,
    LoadDetailView,
    BookLoadView,
    MyBookingsListView
)

urlpatterns = [
    # Consignor URLs
    path('my-loads/', MyLoadsListView.as_view(), name='my_loads'),
    path('loads/create/', LoadCreateView.as_view(), name='load_create'),
    
    # Carrier URLs
    path('loads/available/', AvailableLoadsListView.as_view(), name='available_loads'),
    path('loads/<int:pk>/book/', BookLoadView.as_view(), name='book_load'),
    path('my-bookings/', MyBookingsListView.as_view(), name='my_bookings'),

    # Common URL
    path('loads/<int:pk>/', LoadDetailView.as_view(), name='load_detail'),
]