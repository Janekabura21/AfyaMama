from django import forms
from .models import  ChildProfile, HealthRecord, MaternalProfile, HospitalUser, MotherChildRecord, Patient, Appointment, PhysicalExamination, PreviousPregnancy
from .models import PreviousPregnancy


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
#  Maternal Profile Form



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
        fields = ["hospital", "patient", "maternal_profile", "doctor", "date", "status", "attended", "notes"]
        widgets = {
            'hospital': forms.Select(attrs={'class': 'form-control'}),
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'maternal_profile': forms.Select(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'attended': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date is None:
            raise forms.ValidationError("Please select a valid date.")
        return date




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
        fields = [
            'child', 'vaccine_type', 'date_administered', 'next_due_date',
            'dose_number', 'batch_number', 'administered_by', 'notes'
        ]
        widgets = {
            'date_administered': forms.DateInput(attrs={'type': 'date'}),
            'next_due_date': forms.DateInput(attrs={'type': 'date'}),
        }










