from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import HospitalUser

class HospitalRegistrationForm(UserCreationForm):
    hospital_name = forms.CharField(max_length=255)
    code = forms.CharField(max_length=20, unique=True)
    location = forms.CharField(max_length=255)
    contact_number = forms.CharField(max_length=15)

    class Meta:
        model = HospitalUser
        fields = ['username', 'hospital_name', 'hospital_code', 'location', 'contact_number', 'password1', 'password2']

class HospitalLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
