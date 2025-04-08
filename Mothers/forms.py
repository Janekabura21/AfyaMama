# Mothers/forms.py

from django import forms

class MotherRegistrationForm(forms.Form):
    hospital_code = forms.CharField(label="Hospital Code")
    hospital_name = forms.CharField(label="Hospital Name")
    mother_name = forms.CharField(label="Mother's Full Name")
    identification_number = forms.CharField(label="Identification Number")




class MotherPasswordSetupForm(forms.Form):
    name = forms.CharField(max_length=100)
    identification_number = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
