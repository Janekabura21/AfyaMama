

# Create your models here.
from django.db import models
from django.conf import settings


from django.apps import apps

def get_hospital_model():
    return apps.get_model('MamaCare', 'HospitalUser')

def get_doctor_model():
    return apps.get_model('MamaCare', 'doctor')


class MaternalProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE,
        related_name="maternal_profile"
    )
    # user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to user account
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gravida = models.IntegerField()  # Number of pregnancies
    parity = models.IntegerField()   # Number of births
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField()
    lmp = models.DateField()  # Last Menstrual Period
    edd = models.DateField()  # Estimated Due Date
    marital_status = models.CharField(max_length=50, choices=[
        ('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced')
    ])
    county = models.CharField(max_length=50)
    subcounty = models.CharField(max_length=50, null=True, blank=True)
    ward = models.CharField(max_length=50, null=True, blank=True)
    town_village = models.CharField(max_length=100, null=True, blank=True)
    physical_address = models.CharField(max_length=100, null=True, blank=True)
    telephone = models.CharField(max_length=15)
    id_number = models.CharField(max_length=20, null=True, blank=True)
    huduma_number = models.CharField(max_length=20, null=True, blank=True)
    education_level = models.CharField(max_length=50, null=True, blank=True)
    
    # Next of Kin
    next_of_kin_name = models.CharField(max_length=100)
    next_of_kin_relationship = models.CharField(max_length=50)
    next_of_kin_phone = models.CharField(max_length=15)

    # Medical & Surgical History
    surgical_operation = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)
    hypertension = models.BooleanField(default=False)
    blood_transfusion = models.BooleanField(default=False)
    drug_allergy = models.BooleanField(default=False)
    other_allergies = models.TextField(null=True, blank=True)
    family_history_twins = models.BooleanField(default=False)
    family_history_tb = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.edd}"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]

    mother = models.ForeignKey(MaternalProfile, on_delete=models.CASCADE)
    hospital = models.ForeignKey('MamaCare.HospitalUser', on_delete=models.CASCADE)
    doctor = models.ForeignKey('MamaCare.doctor', on_delete=models.CASCADE)
    date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    attended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mother.name} - {self.date} ({self.status})"

class Notification(models.Model):
    mother = models.ForeignKey(MaternalProfile, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.mother.name} - {'Read' if self.is_read else 'Unread'}"


class Vaccination(models.Model):  # ✅ Ensure this class exists!
    mother = models.ForeignKey(MaternalProfile, on_delete=models.CASCADE)
    date = models.DateField()