
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class HospitalUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class HospitalUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('Doctor', 'Doctor'),
        ('Nurse', 'Nurse'),
        ('Admin', 'Admin'),
    ]

    
    hospital_name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    address = models.TextField()
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"  # Use email for authentication
    REQUIRED_FIELDS = ["username", "hospital_name", "code", "role", "phone_number"]

    objects = HospitalUserManager() 

    def __str__(self):
        return f"{self.email} - {self.role} at {self.hospital_name}"





    
class Patient(models.Model):
    hospital = models.ForeignKey(HospitalUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    contact_number = models.CharField(max_length=15)
    medical_history = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.hospital.name}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("Upcoming", "Upcoming"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    hospital = models.ForeignKey(HospitalUser, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Upcoming")

    def __str__(self):
        return f"Appointment: {self.patient.name} on {self.date}"



class MaternalProfile(models.Model):
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
