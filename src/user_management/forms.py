from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    contact = forms.CharField(max_length=15)
    address = forms.CharField(max_length=255)
    vehicle_type = forms.CharField(max_length=50, required=False)
    vehicle_capacity_kg = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    base_rate_per_km = forms.DecimalField(max_digits=8, decimal_places=2, required=False)
    current_latitude = forms.FloatField(required=False)
    current_longitude = forms.FloatField(required=False)
    user_type = forms.ChoiceField(
        choices=[("carrier", "Carrier"), ("consignor", "Consignor")],
        widget=forms.RadioSelect,
        initial="carrier"
    )
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password1', 'password2',
            'contact', 'address', 'profile_pic', 'user_type',
            'vehicle_type', 'vehicle_capacity_kg', 'base_rate_per_km',
            'current_latitude', 'current_longitude'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Name *'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email *'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password *'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password *'}),
            'contact': forms.TextInput(attrs={'placeholder': 'Phone *'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address *'}),
            'vehicle_type': forms.TextInput(attrs={'placeholder': 'Vehicle type (for carriers)'}),
            'vehicle_capacity_kg': forms.NumberInput(attrs={'placeholder': 'Vehicle capacity (kg)'}),
            'base_rate_per_km': forms.NumberInput(attrs={'placeholder': 'Rate per km'}),
            'current_latitude': forms.NumberInput(attrs={'placeholder': 'Current latitude'}),
            'current_longitude': forms.NumberInput(attrs={'placeholder': 'Current longitude'}),
        }

    def clean_username(self):
        name = self.cleaned_data['username']
        import re
        if not re.match(r'^[A-Z][a-zA-Z]*(?: [A-Z][a-zA-Z]*)*$', name):
            raise forms.ValidationError("Name must be only alphabetical and like Rojan Dumaru.")
        return name

    def clean_contact(self):
        contact = self.cleaned_data['contact']
        if not contact.isdigit() or len(contact) != 10:
            raise forms.ValidationError("Phone must be a 10-digit number.")
        return contact

    def save(self, commit=True):
        user = super().save(commit=False)
        user_type = self.cleaned_data['user_type']
        user.user_type = user_type
        # Optional vehicle/location data for carriers
        user.vehicle_type = self.cleaned_data.get("vehicle_type")
        user.vehicle_capacity_kg = self.cleaned_data.get("vehicle_capacity_kg")
        user.base_rate_per_km = self.cleaned_data.get("base_rate_per_km")
        user.current_latitude = self.cleaned_data.get("current_latitude")
        user.current_longitude = self.cleaned_data.get("current_longitude")
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email *', 'required': True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password *', 'required': True, 'id': 'password'})
    )
    USER_CHOICES = [('carrier', 'Carrier'), ('consignor', 'Consignor')]
    user_type = forms.ChoiceField(
        choices=USER_CHOICES,
        widget=forms.RadioSelect,
        initial='carrier',
        label='User Type',
        required=True
    )
    
class ProfileUpdateForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}),
        help_text='Leave blank if you do not want to change the password.'
    )
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'contact', 'email', 'address', 'profile_pic', 'password',
            'vehicle_type', 'vehicle_capacity_kg', 'base_rate_per_km',
            'current_latitude', 'current_longitude'
        ]
        widgets = {
            'username': forms.TextInput(),
            'contact': forms.TextInput(),
            'email': forms.EmailInput(),
            'address': forms.TextInput(),
            'vehicle_type': forms.TextInput(attrs={'placeholder': 'Vehicle type (for carriers)'}),
            'vehicle_capacity_kg': forms.NumberInput(attrs={'placeholder': 'Vehicle capacity (kg)'}),
            'base_rate_per_km': forms.NumberInput(attrs={'placeholder': 'Rate per km'}),
            'current_latitude': forms.NumberInput(attrs={'placeholder': 'Current latitude'}),
            'current_longitude': forms.NumberInput(attrs={'placeholder': 'Current longitude'}),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            if len(password) < 8 or len(password) > 24:
                raise forms.ValidationError("Password must be between 8 and 24 characters.")
        return password
