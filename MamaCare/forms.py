from django import forms
from .models import MaternalProfile

from .models import HospitalUser, Patient, Appointment
from django.contrib.auth.models import User





class HospitalUserForm(forms.ModelForm):
    class Meta:
        model = HospitalUser
        fields = ['hospital_name', 'code', 'role', 'phone_number', 'email', 'is_active']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
            'hospital_name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match.")

        return cleaned_data


# class HospitalRegistrationForm(UserCreationForm):
#     hospital_name = forms.CharField(max_length=255)
#     code = forms.CharField(max_length=20)
#     location = forms.CharField(max_length=255)
#     contact_number = forms.CharField(max_length=15)

#     class Meta:
#         model = HospitalUser  # Use the custom user model
#         fields = ['username', 'email', 'password1', 'password2', 'hospital_name', 'code', 'location', 'contact_number']

#     def clean_code(self):
#         code = self.cleaned_data.get('code')
#         if HospitalUser.objects.filter(code=code).exists():
#             raise forms.ValidationError("This hospital code is already in use.")
#         return code

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.hospital_name = self.cleaned_data['hospital_name']
#         user.code = self.cleaned_data['code']
#         user.location = self.cleaned_data['location']
#         user.contact_number = self.cleaned_data['contact_number']
#         if commit:
#             user.save()
#         return user


# class HospitalRegistrationForm(UserCreationForm):
#     hospital_name = forms.CharField(max_length=255)
#     code = forms.CharField(max_length=20)
    
#     location = forms.CharField(max_length=255)
#     contact_number = forms.CharField(max_length=15)

#     class Meta:
#         model = HospitalUser
#         fields = ['username', 'hospital_name', 'code', 'location', 'contact_number', 'password1', 'password2']

class HospitalLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class MaternalProfileForm(forms.ModelForm):
    class Meta:
        model = MaternalProfile
        fields = '__all__' 


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["hospital", "name", "date_of_birth", "contact_number", "medical_history"]

# Appointment Form
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["hospital", "patient", "date", "status"]


# code = forms.CharField(max_length=20, unique=True)