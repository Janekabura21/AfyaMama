from django import forms
from .models import Appointment, MaternalProfile

class AppointmentForm(forms.ModelForm):
    """Form for booking hospital appointments"""
    class Meta:
        model = Appointment
        fields = ['hospital', 'date', 'time', 'reason']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

class MaternalProfileForm(forms.ModelForm):
    """Form for updating maternal profile"""
    class Meta:
        model = MaternalProfile
        exclude = ['user']  # Exclude user field if linked to auth system
