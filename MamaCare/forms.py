import random
from django import forms
from .models import  ChildProfile, HealthRecord, MaternalProfile, HospitalUser, MotherChildRecord, PhysicalExamination, PreviousPregnancy
from .models import PreviousPregnancy
from django.core.mail import send_mail


# # Hospital User Form
class HospitalRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = HospitalUser
        fields = ['hospital_name', 'code', 'email', 'phone_number']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Hash password
        if commit:
            user.save()
        return user
    

#     def send_otp(self):
#         otp = str(random.randint(100000, 999999))  # Generate a random OTP
#         subject = "Your OTP for Hospital Registration"
#         message = f"Your OTP is {otp}. Please use it to confirm your registration."
#         recipient_list = [self.cleaned_data['email']]  # Send OTP to the user's email

#         # Send the email
#         send_mail(subject, message, 'admin@yourdomain.com', recipient_list)
#         return otp

# ----------------------------
# 2. HospitalUser Admin Form
# ----------------------------
class HospitalUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_repeat = forms.CharField(widget=forms.PasswordInput)
    otp = forms.CharField(max_length=6, required=False)

    class Meta:
        model = HospitalUser
        fields = ['email', 'hospital_name', 'code', 'phone_number', 'password']

    def clean_password_repeat(self):
        password = self.cleaned_data.get("password")
        password_repeat = self.cleaned_data.get("password_repeat")

        if password != password_repeat:
            raise forms.ValidationError("Passwords do not match")
        return password_repeat

    def send_otp(self):
        otp = str(random.randint(100000, 999999))  # Generate a random OTP
        subject = "Your OTP for Hospital Registration"
        message = f"Your OTP is {otp}. Please use it to confirm your registration."
        recipient_list = [self.cleaned_data['email']]  # Send OTP to the user's email

        # Send the email
        send_mail(subject, message, 'kaburajane978@gmail.com', recipient_list)
        return otp
# 3. User Registration Form (for new users)
# ----------------------------
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
        required=False,
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
        if code and HospitalUser.objects.filter(code=code).exists():
            raise forms.ValidationError("This hospital code is already in use.")
        return code
    

from django import forms
from django.contrib.auth import authenticate

class HospitalLoginForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        # Check if the email and password combination is valid
        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError("Invalid email or password.")
        return cleaned_data



class MaternalProfileForm(forms.ModelForm):
    class Meta:
        model = MaternalProfile
        fields = '__all__'
        widgets = {
            
    
    
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'lmp': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'edd': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
        }


# Patient Form



# Appointment Form



class PreviousPregnancyForm(forms.ModelForm):
    class Meta:
        model = PreviousPregnancy
        fields = '__all__'





class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = '__all__'




# class MotherForm(forms.ModelForm):
#     class Meta:
#         model = Mother
#         fields = ['name', 'identification_number', 'medical_history']

# class ChildForm(forms.ModelForm):
#     class Meta:
#         model = Child
#         fields = ['name', 'date_of_birth']

class RecordForm(forms.ModelForm):
    class Meta:
        model = MotherChildRecord
        fields = ['category', 'details']



class PhysicalExaminationForm(forms.ModelForm):
    class Meta:
        model = PhysicalExamination
        fields = '__all__'
        widgets = {
            'ipt_given_date': forms.DateInput(attrs={'type': 'date'}),
            'ipt_next_visit': forms.DateInput(attrs={'type': 'date'}),
            'scan_first_date': forms.DateInput(attrs={'type': 'date'}),
            'scan_second_date': forms.DateInput(attrs={'type': 'date'}),
        }






class ChildProfileForm(forms.ModelForm):
    class Meta:
        model = ChildProfile
        
        fields = "__all__"  # Includes all fields from the model
        widgets = {
            
    
    
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'date_first_seen': forms.DateInput(attrs={'type': 'date'}),
            'date_of_registration': forms.DateInput(attrs={'type': 'date'}),
        }






from django import forms
from .models import Immunization

class ImmunizationForm(forms.ModelForm):
    class Meta:
        model = Immunization
        exclude = ['child']  # Don't include this in the form UI
        widgets = {
            # Date fields
            'bcg_date_given': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'bcg_next_visit': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            # Add all other date fields similarly
            
            # Text inputs
            'batch_number': forms.TextInput(attrs={'class': 'form-control'}),
            'administered_by': forms.TextInput(attrs={'class': 'form-control'}),
            
            # Textareas
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'aefi_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            
            # Selects
            'pcv_injection_site': forms.Select(attrs={'class': 'form-control'}),
            'rota_reaction': forms.Select(attrs={'class': 'form-control'}),
            
            # Checkboxes/radios
            'bcg_scar_present': forms.RadioSelect(choices=[(True, 'PRESENT'), (False, 'ABSENT')]),
            'yf_eligible': forms.CheckboxInput(),
            'aefi_reported': forms.CheckboxInput(),
        }
