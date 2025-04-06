
from datetime import date, datetime
from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.forms import ValidationError
import datetime



# MamaCare/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
# MamaCare/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class HospitalUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class HospitalUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    hospital_name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=50, blank=True, null=True)

    objects = HospitalUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['hospital_name']

    def __str__(self):
        return self.email



    


def generate_temp_id():
    return "TMP-" + str(uuid.uuid4())[:8]

from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

class MaternalProfile(models.Model):
    # Remove mother_id completely and use identification_number as primary key
    identification_number = models.CharField(
        max_length=20,
        primary_key=True,
        verbose_name="Mother ID/National ID"
    )
    name = models.CharField(max_length=100)
    hospital = models.ForeignKey(
        'HospitalUser',
        on_delete=models.CASCADE,
        related_name='mothers_profiles',
        default=1
    )    
    date_of_birth = models.DateField(null=True, blank=True)
    gravida = models.IntegerField()  # Number of pregnancies
    parity = models.IntegerField()  # Number of births
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
    guardian_id = models.CharField(max_length=20, blank=True, null=True)
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

    @property
    def age(self):
        """Calculate age safely handling None values"""
        if not self.date_of_birth:
            return None
        today = date.today()
        return (today - self.date_of_birth).days // 365
    
    def clean(self):
        """Validate age requirements with safe age checking"""
        age = self.age
        
        if age is not None:
            if age >= 18 and not self.identification_number:
                raise ValidationError("Adults must provide an ID number.")
            if age < 18 and not self.guardian_id:
                raise ValidationError("Minors must provide a guardian ID number.")
                
        # Additional validation for identification_number format if needed
        if self.identification_number and len(self.identification_number) < 5:
            raise ValidationError("ID number must be at least 5 characters")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} (ID: {self.identification_number}) - EDD: {self.edd}"
    
    
    


class ChildProfile(models.Model):
    # Replace default ID with mother's ID as primary key
    id = models.CharField(
        primary_key=True,
        max_length=20,
        verbose_name="Mother's ID Number",
        help_text="Unique identification number of the mother"
    )
    mothers_profile = models.ForeignKey(
        MaternalProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        to_field='identification_number',
        related_name='children',
        db_column='mother_id'
    )
    
    
    # Keep all your existing fields (unchanged)
    name = models.CharField(max_length=100)
    sex = models.CharField(max_length=10, choices=[("Male", "Male"), ("Female", "Female")])
    date_of_birth = models.DateField(null=False, blank=False, default=datetime.date.today)
    gestation_at_birth = models.PositiveIntegerField(null=True, blank=True)  # Weeks
    birth_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # in grams
    birth_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # in cm
    birth_order = models.PositiveIntegerField(null=True, blank=True)
    date_first_seen = models.DateField(null=False, blank=False, default=datetime.date.today)
    
    # Health Record of Child
    place_of_birth = models.CharField(max_length=20, choices=[("Home", "Home"), ("Hospital", "Hospital"), ("Other", "Other")])
    health_facility_name = models.CharField(max_length=100, null=True, blank=True)
    birth_notification_no = models.CharField(max_length=20, null=True, blank=True)
    immunization_registration_no = models.CharField(max_length=20, null=True, blank=True)
    child_welfare_clinic_no = models.CharField(max_length=20, null=True, blank=True)
    master_facility_code = models.CharField(max_length=20, null=True, blank=True)
    
    # Civil Registration
    birth_certificate_no = models.CharField(max_length=20, null=True, blank=True)
    date_of_registration = models.DateField(null=True, blank=True)
    place_of_registration = models.CharField(max_length=100, null=True, blank=True)
    
    # Parent/Guardian Information
    fathers_name = models.CharField(max_length=100, null=True, blank=True)
    fathers_phone = models.CharField(max_length=20, null=True, blank=True)
    mothers_phone = models.CharField(max_length=20)
    # Remove mother_id_number since we're using it as primary key now
    guardian_name = models.CharField(max_length=100, null=True, blank=True)
    guardian_phone = models.CharField(max_length=20, null=True, blank=True)
    
    # Address Details
    residence = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    division = models.CharField(max_length=100, null=True, blank=True)
    sub_county = models.CharField(max_length=100, null=True, blank=True)
    town = models.CharField(max_length=100, null=True, blank=True)
    estate_village = models.CharField(max_length=100, null=True, blank=True)
    postal_address = models.CharField(max_length=100, null=True, blank=True)
    
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Child Profile"
        verbose_name_plural = "Child Profiles"
        ordering = ['date_of_birth']
    
    def clean(self):
        """Validate that mother's ID is properly set"""
        if not self.id:
            # Get mother's ID from the profile if not set
            if self.mothers_profile:
                self.id = self.mothers_profile.identification_number
            else:
                raise ValidationError("Mother's identification number is required")
        
        # Ensure mother's ID matches the linked profile
        if self.mothers_profile and self.id != self.mothers_profile.identification_number:
            raise ValidationError({
                'id': "Mother's ID must match the linked maternal profile ID"
            })
    
    def save(self, *args, **kwargs):
        """Automatically set mother's ID from profile if not provided"""
        self.full_clean()  # Run validation
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} (Mother ID: {self.id})"





class PreviousPregnancy(models.Model):
    mother = models.ForeignKey(
        MaternalProfile,
        on_delete=models.CASCADE, 
        related_name="previous_pregnancies",
        to_field='identification_number')
    pregnancy_order = models.IntegerField()
    year = models.IntegerField()
    anc_visits = models.IntegerField()
    place_of_birth = models.CharField(max_length=255)
    gestation_weeks = models.IntegerField()
    labour_duration = models.CharField(max_length=50)
    mode_of_delivery = models.CharField(max_length=50)
    birth_weight = models.IntegerField()
    sex = models.CharField(max_length=10)
    outcome = models.CharField(max_length=50)
    puerperium = models.CharField(max_length=50)

    def __str__(self):
        return f"Pregnancy {self.pregnancy_order} - {self.mother.name}"
    









class HealthRecord(models.Model):
    mother = models.ForeignKey(MaternalProfile, on_delete=models.CASCADE, related_name="health_records", null=True, blank=True)
    child = models.ForeignKey(ChildProfile, on_delete=models.CASCADE, related_name="health_records", null=True, blank=True)
    section = models.CharField(max_length=255, choices=[
        ("ANC, Childbirth and Postnatal Care", "ANC, Childbirth and Postnatal Care"),
        ("Maternal Profile", "Maternal Profile"),
        ("Medical & Surgical History", "Medical & Surgical History"),
        ("Previous Pregnancy", "Previous Pregnancy"),
        ("Antenatal Profile", "Antenatal Profile"),
        ("Weight Monitoring Chart", "Weight Monitoring Chart"),
        ("Clinical Notes", "Clinical Notes"),
        ("Malaria Prophylaxis", "Malaria Prophylaxis"),
        ("Maternal Serology Testing", "Maternal Serology Testing"),
        ("Infant Feeding", "Infant Feeding"),
        ("Danger Signs During Pregnancy", "Danger Signs During Pregnancy"),
        ("Positioning for Breastfeeding", "Positioning for Breastfeeding"),
        ("Child Health Monitoring", "Child Health Monitoring"),
        ("Developmental Milestones", "Developmental Milestones"),
        ("Growth Monitoring", "Growth Monitoring"),
        ("Immunization", "Immunization"),
        ("Vitamin A Supplementation", "Vitamin A Supplementation"),
        ("Deworming", "Deworming"),
        ("PMTCT of HIV/Syphilis/Hepatitis B", "PMTCT of HIV/Syphilis/Hepatitis B"),
        ("Recommendations for Child Care", "Recommendations for Child Care"),
    ])
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.section} - {self.mother if self.mother else self.child}"



class MotherChildRecord(models.Model):
    category = models.CharField(max_length=255)
    details = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category










class PhysicalExamination(models.Model):
    # General Examination
    blood_pressure = models.CharField(max_length=10, help_text="e.g., 118/65 mmHg")
    pulse_rate = models.PositiveIntegerField(help_text="Beats per minute")
    cvs = models.TextField(blank=True, null=True)  # Cardiovascular system
    respiratory_system = models.TextField(blank=True, null=True)
    breasts = models.TextField(blank=True, null=True)
    abdomen = models.TextField(blank=True, null=True)
    genital_examination = models.TextField(blank=True, null=True)
    discharge_or_ulcer = models.BooleanField(default=False, help_text="Check if present")

    # Antenatal Profile
    hemoglobin = models.FloatField(help_text="g/dl")
    blood_group = models.CharField(max_length=3, choices=[("A", "A"), ("B", "B"), ("AB", "AB"), ("O", "O")])
    rhesus_factor = models.CharField(max_length=5, choices=[("TR+", "TR+"), ("TR-", "TR-")])
    urinalysis = models.CharField(max_length=50, blank=True, null=True)
    blood_rbs = models.FloatField(blank=True, null=True, help_text="Random blood sugar")

    # TB Screening
    tb_screening_outcome = models.BooleanField(default=False, help_text="True = Positive, False = Negative")
    ipt_given_date = models.DateField(blank=True, null=True)
    ipt_next_visit = models.DateField(blank=True, null=True)

    # Obstetric Ultrasound
    scan_first_date = models.DateField(blank=True, null=True, help_text="Before 24 weeks")
    scan_second_date = models.DateField(blank=True, null=True, help_text="Third trimester")

    # Triple Testing (HIV, Syphilis, Hep B)
    hiv_status = models.CharField(max_length=20, choices=[("Reactive", "Reactive"), ("Non-Reactive", "Non-Reactive"), ("Not Tested", "Not Tested")], default="Not Tested")
    syphilis_status = models.CharField(max_length=20, choices=[("Reactive", "Reactive"), ("Non-Reactive", "Non-Reactive"), ("Not Tested", "Not Tested")], default="Not Tested")
    hepatitis_b_status = models.CharField(max_length=20, choices=[("Reactive", "Reactive"), ("Non-Reactive", "Non-Reactive"), ("Not Tested", "Not Tested")], default="Not Tested")

    # Partner HIV Testing
    couple_testing_done = models.BooleanField(default=False)
    partner_hiv_status = models.CharField(max_length=20, choices=[("Reactive", "Reactive"), ("Non-Reactive", "Non-Reactive"), ("Not Tested", "Not Tested")], default="Not Tested")

    def __str__(self):
        return f"Physical Examination - BP: {self.blood_pressure}, Pulse: {self.pulse_rate}"















from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import ChildProfile  # Make sure this import works

class Immunization(models.Model):
    VACCINE_CHOICES = [
        ('BCG', 'BCG'),
        ('OPV', 'Oral Polio Vaccine (OPV)'),
        ('IPV', 'Inactivated Polio Vaccine (IPV)'),
        ('PENTA', 'Pentavalent (DPT-HepB-Hib)'),
        ('PCV', 'Pneumococcal Conjugate Vaccine (PCV)'),
        ('ROTA', 'Rotavirus Vaccine'),
        ('MR', 'Measles-Rubella (MR)'),
        ('YF', 'Yellow Fever'),
        ('VIT_A', 'Vitamin A Supplementation'),
        ('DEWORM', 'Deworming'),
    ]
    REACTION_CHOICES = [
        ('NONE', 'None'),
        ('MILD', 'Mild (vomiting)'),
        ('MODERATE', 'Moderate (diarrhea)'),
        ('SEVERE', 'Severe (intussusception)'),
    ]
    
    child = models.OneToOneField(
        ChildProfile, 
        on_delete=models.CASCADE,
        related_name='immunizations',
        to_field='id'
    )
    # BCG Fields
    bcg_date_given = models.DateField(null=True, blank=True)
    bcg_next_visit = models.DateField(null=True, blank=True)
    bcg_scar_checked = models.DateField(null=True, blank=True)
    bcg_scar_present = models.BooleanField(null=True, blank=True)
    bcg_repeated_date = models.DateField(null=True, blank=True)
    
    # Polio Fields
    opv_birth_date = models.DateField(null=True, blank=True)
    opv_birth_next_date = models.DateField(null=True, blank=True)
    opv1_date = models.DateField(null=True, blank=True)
    opv1_next_date = models.DateField(null=True, blank=True)
    opv2_date = models.DateField(null=True, blank=True)
    opv2_next_date = models.DateField(null=True, blank=True)
    opv3_date = models.DateField(null=True, blank=True)
    opv3_next_date = models.DateField(null=True, blank=True)
    ipv_date = models.DateField(null=True, blank=True)
    ipv_next_date = models.DateField(null=True, blank=True)
    
    # Pentavalent Fields
    penta1_date = models.DateField(null=True, blank=True)
    penta1_next_date = models.DateField(null=True, blank=True)
    penta2_date = models.DateField(null=True, blank=True)
    penta2_next_date = models.DateField(null=True, blank=True)
    penta3_date = models.DateField(null=True, blank=True)
    penta3_next_date = models.DateField(null=True, blank=True)
    
    # PCV Fields
    pcv1_date = models.DateField(null=True, blank=True)
    pcv1_next_date = models.DateField(null=True, blank=True)
    pcv2_date = models.DateField(null=True, blank=True)
    pcv2_next_date = models.DateField(null=True, blank=True)
    pcv3_date = models.DateField(null=True, blank=True)
    pcv3_next_date = models.DateField(null=True, blank=True)
    pcv_injection_site = models.CharField(max_length=50, null=True, blank=True)
    
    # Rotavirus Fields
    rota1_date = models.DateField(null=True, blank=True)
    rota1_next_date = models.DateField(null=True, blank=True)
    rota2_date = models.DateField(null=True, blank=True)
    rota2_next_date = models.DateField(null=True, blank=True)
    rota3_date = models.DateField(null=True, blank=True)
    rota3_next_date = models.DateField(null=True, blank=True)
    rota_administered_by = models.CharField(max_length=100, null=True, blank=True)
    rota_reaction = models.CharField(max_length=20, choices=REACTION_CHOICES, null=True, blank=True)
    
    # MR Fields
    mr6_date = models.DateField(null=True, blank=True)
    mr6_next_date = models.DateField(null=True, blank=True)
    mr9_date = models.DateField(null=True, blank=True)
    mr9_next_date = models.DateField(null=True, blank=True)
    mr18_date = models.DateField(null=True, blank=True)
    mr18_next_date = models.DateField(null=True, blank=True)
    
    # Yellow Fever Fields
    yf_date = models.DateField(null=True, blank=True)
    yf_next_date = models.DateField(null=True, blank=True)
    yf_eligible = models.BooleanField(null=True, blank=True)
    
    # Other Vaccines
    other_vaccine1_name = models.CharField(max_length=100, null=True, blank=True)
    other_vaccine1_date = models.DateField(null=True, blank=True)
    other_vaccine2_name = models.CharField(max_length=100, null=True, blank=True)
    other_vaccine2_date = models.DateField(null=True, blank=True)
    
    # Adverse Events
    aefi_date = models.DateField(null=True, blank=True)
    aefi_description = models.TextField(null=True, blank=True)
    aefi_vaccine = models.CharField(max_length=100, null=True, blank=True)
    aefi_batch_number = models.CharField(max_length=50, null=True, blank=True)
    aefi_manufacturer = models.CharField(max_length=100, null=True, blank=True)
    aefi_manufacture_date = models.DateField(null=True, blank=True)
    aefi_expiry_date = models.DateField(null=True, blank=True)
    aefi_reported = models.BooleanField(default=False)
    
    # Vitamin A
    vita6_age_given = models.CharField(max_length=50, null=True, blank=True)
    vita6_date_given = models.DateField(null=True, blank=True)
    vita6_next_date = models.DateField(null=True, blank=True)
    vita12_age_given = models.CharField(max_length=50, null=True, blank=True)
    vita12_date_given = models.DateField(null=True, blank=True)
    vita12_next_date = models.DateField(null=True, blank=True)
    vita18_age_given = models.CharField(max_length=50, null=True, blank=True)
    vita18_date_given = models.DateField(null=True, blank=True)
    vita18_next_date = models.DateField(null=True, blank=True)
    vita24_age_given = models.CharField(max_length=50, null=True, blank=True)
    vita24_date_given = models.DateField(null=True, blank=True)
    vita24_next_date = models.DateField(null=True, blank=True)
    vita30_age_given = models.CharField(max_length=50, null=True, blank=True)
    vita30_date_given = models.DateField(null=True, blank=True)
    vita30_next_date = models.DateField(null=True, blank=True)
    vita36_age_given = models.CharField(max_length=50, null=True, blank=True)
    vita36_date_given = models.DateField(null=True, blank=True)
    vita36_next_date = models.DateField(null=True, blank=True)
    
    # Micronutrient Powders
    mnp_month6_issued = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MaxValueValidator(10)])
    mnp_month6_date = models.DateField(null=True, blank=True)
    mnp_month6_next_date = models.DateField(null=True, blank=True)
    # Repeat for months 7-23
    
    # Deworming
    deworm12_age_given = models.CharField(max_length=50, null=True, blank=True)
    deworm12_date_given = models.DateField(null=True, blank=True)
    deworm12_next_date = models.DateField(null=True, blank=True)
    deworm12_dosage = models.CharField(max_length=20, null=True, blank=True)
    deworm18_age_given = models.CharField(max_length=50, null=True, blank=True)
    deworm18_date_given = models.DateField(null=True, blank=True)
    deworm18_next_date = models.DateField(null=True, blank=True)
    deworm18_dosage = models.CharField(max_length=20, null=True, blank=True)
    deworm24_age_given = models.CharField(max_length=50, null=True, blank=True)
    deworm24_date_given = models.DateField(null=True, blank=True)
    deworm24_next_date = models.DateField(null=True, blank=True)
    deworm24_dosage = models.CharField(max_length=20, null=True, blank=True)
    deworm30_age_given = models.CharField(max_length=50, null=True, blank=True)
    deworm30_date_given = models.DateField(null=True, blank=True)
    deworm30_next_date = models.DateField(null=True, blank=True)
    deworm30_dosage = models.CharField(max_length=20, null=True, blank=True)
    
    # Common fields
    batch_number = models.CharField(max_length=50, null=True, blank=True)
    administered_by = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Immunization for {self.child} on {self.created_at}"
    

class Doctor(models.Model):
    hospital = models.ForeignKey(HospitalUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"

class Appointment(models.Model):
    hospital = models.ForeignKey(HospitalUser, on_delete=models.CASCADE)
    maternal_profile = models.ForeignKey('MaternalProfile', on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])
    attended = models.BooleanField(null=True, blank=True)