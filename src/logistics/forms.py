from django import forms
from .models import Load

class LoadForm(forms.ModelForm):
    class Meta:
        model = Load
        fields = [
            'name', 'description', 'pickup_address', 'pickup_latitude', 'pickup_longitude',
            'destination_address', 'destination_latitude', 'destination_longitude',
            'weight', 'scheduled_date'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Load Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe the contents of the load'}),
            'pickup_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Pickup Address'}),
            'pickup_latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'placeholder': 'Pickup latitude'}),
            'pickup_longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'placeholder': 'Pickup longitude'}),
            'destination_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Destination Address'}),
            'destination_latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'placeholder': 'Destination latitude'}),
            'destination_longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'placeholder': 'Destination longitude'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight in KG'}),
            'scheduled_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
