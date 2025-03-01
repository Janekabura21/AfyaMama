from django import forms
from .models import MaternalProfile, HospitalUser, Patient, Appointment



# Hospital User Form
class HospitalUserForm(forms.ModelForm):
    class Meta:
        model = HospitalUser
        fields = ['hospital_name', 'code', 'role', 'phone_number', 'email', 'address', 'is_active', 'is_staff', 'is_superuser']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
            'hospital_name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_code(self):
        code = self.cleaned_data.get('code')
        
        # If code is provided, check uniqueness
        if code and HospitalUser.objects.filter(code=code).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This hospital code is already in use.")
        
        return code
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        return phone if phone else None 



# class HospitalUserForm(forms.ModelForm):
#     class Meta:
#         model = HospitalUser
#         fields = ['hospital_name', 'code', 'role', 'phone_number', 'email', 'address', 'is_active', 'is_staff', 'is_superuser']
#         widgets = {
#             'role': forms.Select(attrs={'class': 'form-control'}),
#             'hospital_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'code': forms.TextInput(attrs={'class': 'form-control'}),
#             'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
#             'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#             'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#             'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#         }

#     def clean_code(self):
#         code = self.cleaned_data.get('code')
#         if HospitalUser.objects.filter(code=code).exclude(pk=self.instance.pk).exists():
#             raise forms.ValidationError("This hospital code is already in use.")
#         return code



# User Registration Form

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Password"
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm Password"
    )
    code = forms.CharField(
        required=False,  # Optional because model can auto-generate it
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Hospital Code"
    )

    class Meta:
        model = HospitalUser
        fields = ['email', 'password', 'code']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match.")

        return cleaned_data

    def clean_code(self):
        code = self.cleaned_data.get("code")
        
        # If code is provided, ensure it's unique
        if code and HospitalUser.objects.filter(code=code).exists():
            raise forms.ValidationError("This hospital code is already in use.")

        return code



# class UserRegistrationForm(forms.ModelForm):
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={'class': 'form-control'}),
#         label="Password"
#     )
#     password_confirm = forms.CharField(
#         widget=forms.PasswordInput(attrs={'class': 'form-control'}),
#         label="Confirm Password"
#     )

#     class Meta:
#         model = HospitalUser
#         fields = ['email', 'password']
#         widgets = {
            
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         password_confirm = cleaned_data.get("password_confirm")

#         if password and password_confirm and password != password_confirm:
#             self.add_error('password_confirm', "Passwords do not match.")

#         return cleaned_data


# Hospital Login Form
class HospitalLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Password"
    )


# Maternal Profile Form
class MaternalProfileForm(forms.ModelForm):
    class Meta:
        model = MaternalProfile
        fields = '__all__'


# Patient Form
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["hospital", "name", "date_of_birth", "contact_number", "medical_history"]
        widgets = {
            'hospital': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'medical_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# Appointment Form
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["hospital", "patient", "date", "status"]
        widgets = {
            'hospital': forms.Select(attrs={'class': 'form-control'}),
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }














# from django import forms
# from .models import MaternalProfile

# from .models import HospitalUser, Patient, Appointment
# from django.contrib.auth.models import User





# class HospitalUserForm(forms.ModelForm):
#     class Meta:
#         model = HospitalUser
#         fields = ['hospital_name', 'code', 'role', 'phone_number', 'email', 'is_active']
#         widgets = {
#             'role': forms.Select(attrs={'class': 'form-control'}),
#             'hospital_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'code': forms.TextInput(attrs={'class': 'form-control'}),
#             'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
#             'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#         }



# class UserRegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         password_confirm = cleaned_data.get("password_confirm")

#         if password != password_confirm:
#             self.add_error('password_confirm', "Passwords do not match.")

#         return cleaned_data


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

# class HospitalLoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)


# class MaternalProfileForm(forms.ModelForm):
#     class Meta:
#         model = MaternalProfile
#         fields = '__all__' 


# class PatientForm(forms.ModelForm):
#     class Meta:
#         model = Patient
#         fields = ["hospital", "name", "date_of_birth", "contact_number", "medical_history"]

# # Appointment Form
# class AppointmentForm(forms.ModelForm):
#     class Meta:
#         model = Appointment
#         fields = ["hospital", "patient", "date", "status"]


# # code = forms.CharField(max_length=20, unique=True)