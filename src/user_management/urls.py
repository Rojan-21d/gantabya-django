from django.urls import path
from .views import CustomLogoutView, LoginView, ProfileUpdateView, RegisterView, HomeView

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name='register'),
    path('home/', HomeView.as_view(), name='home'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
