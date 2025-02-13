from django import forms
from .models import MaternalProfile, HealthFacility


class HealthFacilityForm(forms.ModelForm):
    class Meta:
        model = HealthFacility
        fields = ['name', 'code']

class MaternalProfileForm(forms.ModelForm):
    class Meta:
        model = MaternalProfile
        fields = '__all__'  # Include all fields from the model
