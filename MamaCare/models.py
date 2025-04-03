
from datetime import date, datetime
from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.forms import ValidationError
import datetime

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
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"  # Use email for authentication
    REQUIRED_FIELDS = ["hospital_name", "code", "role", "phone_number"]

    objects = HospitalUserManager() 


    def save(self, *args, **kwargs):
        if not self.code:  # Auto-generate unique code if blank
            self.code = str(uuid.uuid4())[:10]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} - {self.role} at {self.hospital_name}"





    
class Patient(models.Model):
    hospital = models.ForeignKey(HospitalUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    contact_number = models.CharField(max_length=15)
    medical_history = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.hospital.hospital_name}"

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
        'MaternalProfile',
        on_delete=models.CASCADE,
        to_field='identification_number',
        related_name='children'
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


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
        ("Cancelled", "Cancelled"),
        ("Completed", "Completed"),
    ]

    hospital = models.ForeignKey(HospitalUser, on_delete=models.CASCADE, related_name="appointments")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    maternal_profile = models.ForeignKey(MaternalProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="appointments")
    doctor = models.ForeignKey(HospitalUser, on_delete=models.CASCADE, related_name="doctor_appointments", limit_choices_to={'role': 'Doctor'}, null=True, blank=True)
    date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    attended = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        doctor_name = self.doctor.hospital_name if self.doctor else "Unassigned"
        return f"Appointment: {self.patient.name} with {doctor_name} on {self.date}"


class Doctor(models.Model):
    user = models.OneToOneField(HospitalUser, on_delete=models.CASCADE, related_name="doctor_profile")
    specialization = models.CharField(max_length=255)
    experience_years = models.IntegerField()
    qualifications = models.TextField()
    availability = models.CharField(
        max_length=50,
        choices=[
            ("Full-time", "Full-time"),
            ("Part-time", "Part-time"),
            ("Consultant", "Consultant"),
        ],
        default="Full-time",
    )

    def __str__(self):
        return f"Dr. {self.user.hospital_name} - {self.specialization}"



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
    
    child = models.ForeignKey(
        ChildProfile, 
        on_delete=models.CASCADE,
        related_name='immunizations',
        to_field='id'
    )
    vaccine_type = models.CharField(max_length=10, choices=VACCINE_CHOICES)
    date_administered = models.DateField()
    next_due_date = models.DateField(null=True, blank=True)
    dose_number = models.PositiveSmallIntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(3)]
    )
    dose_amount = models.CharField(max_length=50, null=True, blank=True)
    batch_number = models.CharField(max_length=50, null=True, blank=True)
    administered_by = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    
    # BCG-specific fields
    scar_checked = models.BooleanField(null=True, blank=True)
    scar_present = models.BooleanField(null=True, blank=True)
    date_repeated = models.DateField(null=True, blank=True)
    
    # Vitamin A specific
    vitamin_a_dose = models.CharField(max_length=20, null=True, blank=True, choices=[
        ('100000IU', '100,000 IU (6 months)'),
        ('200000IU', '200,000 IU (12+ months)'),
    ])
    vitamin_a_age_given = models.CharField(max_length=50, null=True, blank=True)
    
    # Deworming specific
    deworming_medication = models.CharField(max_length=50, null=True, blank=True, default='Albendazole')
    deworming_dosage = models.CharField(max_length=50, null=True, blank=True, choices=[
        ('200mg', '200mg (1-2 years)'),
        ('400mg', '400mg (2+ years)'),
    ])
    deworming_age_given = models.CharField(max_length=50, null=True, blank=True)
    
    # MR Vaccine specific
    mr_dose_age = models.CharField(max_length=20, null=True, blank=True, choices=[
        ('6m', '6 months'),
        ('9m', '9 months'),
        ('18m', '18 months'),
    ])
    
    # Yellow Fever specific
    yf_eligible = models.BooleanField(null=True, blank=True)
    
    class Meta:
        ordering = ['date_administered']
        verbose_name = "Immunization Record"
        verbose_name_plural = "Immunization Records"


    def get_mother_id(self):
        """Helper method to directly access mother's ID"""
        return self.child.id
    
    def clean(self):
        """Additional validation"""
        if not self.child_id:
            raise ValidationError("Child/Mother ID is required")
        
        # Vaccine-specific validations
        if self.vaccine_type == 'BCG' and not self.scar_checked:
            raise ValidationError("Scar check status is required for BCG vaccine")
    
    def clean(self):
        """Validate vaccine-specific requirements"""
        if self.vaccine_type == 'BCG' and not self.scar_checked:
            raise ValidationError("Scar check status is required for BCG vaccine")
        
        if self.vaccine_type == 'VIT_A' and not self.vitamin_a_dose:
            raise ValidationError("Vitamin A dose is required")
            
        if self.vaccine_type == 'DEWORM' and not self.deworming_dosage:
            raise ValidationError("Deworming dosage is required")
    
    def __str__(self):
        return f"{self.get_vaccine_type_display()} for {self.child.name} on {self.date_administered}"

class MicronutrientPowder(models.Model):
    child = models.ForeignKey(ChildProfile, on_delete=models.CASCADE, related_name='mnps' ,
        to_field='id' )
    month = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(6), MaxValueValidator(23)]
    )
    sachets_issued = models.PositiveSmallIntegerField(
        default=10,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    date_issued = models.DateField()
    next_visit_date = models.DateField()
    notes = models.TextField(null=True, blank=True)
    
    class Meta:
        unique_together = ('child', 'month')
        ordering = ['month']
    
    def __str__(self):
        return f"MNP for {self.child.name} at {self.month} months"

class HIVInfantTesting(models.Model):
    TEST_TYPES = [
        ('1st_pcr', '1st DNA PCR'),
        ('confirm_pcr', 'Confirmatory DNA PCR'),
        ('2nd_pcr', '2nd DNA PCR (6 months)'),
        ('3rd_pcr', '3rd DNA PCR (12 months)'),
        ('antibody_18m', 'Antibody test (18 months)'),
        ('antibody_24m', 'Antibody test (24 months)'),
        ('final_antibody', 'Final antibody test (6 weeks post-weaning)'),
    ]
    
    child = models.ForeignKey(ChildProfile, on_delete=models.CASCADE, related_name='hiv_tests',
        to_field='id' )
    test_type = models.CharField(max_length=20, choices=TEST_TYPES)
    sample_date = models.DateField()
    result = models.CharField(max_length=20, choices=[
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('pending', 'Pending'),
        ('indeterminate', 'Indeterminate'),
    ])
    viral_load = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ['sample_date']
    
    def __str__(self):
        return f"{self.get_test_type_display()} for {self.child.name}"

class ARVProphylaxis(models.Model):
    child = models.ForeignKey(ChildProfile, on_delete=models.CASCADE, related_name='arv_prophylaxis')
    start_date = models.DateField()
    regimen = models.CharField(max_length=100, default='AZT+NVP')
    status = models.CharField(max_length=20, choices=[
        ('continuing', 'Continuing'),
        ('stopped', 'Stopped (HIV+)'),
        ('completed', 'Completed'),
    ])
    discontinuation_date = models.DateField(null=True, blank=True)
    discontinuation_reason = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = "ARV Prophylaxis"
        verbose_name_plural = "ARV Prophylaxes"
    
    def __str__(self):
        return f"ARV for {self.child.name} ({self.get_status_display()})"

class ARTRegimen(models.Model):
    child = models.ForeignKey(ChildProfile, on_delete=models.CASCADE, related_name='art_regimens')
    start_date = models.DateField()
    regimen = models.CharField(max_length=100)
    current_dose = models.CharField(max_length=100)
    last_viral_load = models.PositiveIntegerField(null=True, blank=True)
    last_vl_date = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = "ART Regimen"
        ordering = ['-start_date']
    
    def __str__(self):
        return f"ART for {self.child.name} ({self.regimen})"

class CTXProphylaxis(models.Model):
    child = models.ForeignKey(ChildProfile, on_delete=models.CASCADE, related_name='ctx_prophylaxis')
    start_date = models.DateField()
    dose = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('discontinued', 'Discontinued'),
        ('completed', 'Completed'),
    ])
    discontinuation_date = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = "CTX Prophylaxis"
        verbose_name_plural = "CTX Prophylaxes"
    
    def __str__(self):
        return f"CTX for {self.child.name} ({self.get_status_display()})"

class InfantIPT(models.Model):
    child = models.ForeignKey(ChildProfile, on_delete=models.CASCADE, related_name='ipt_records')
    eligible = models.BooleanField(default=False)
    start_date = models.DateField(null=True, blank=True)
    dose = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('completed', 'Completed'),
    ], null=True, blank=True)
    
    class Meta:
        verbose_name = "Infant IPT"
        verbose_name_plural = "Infant IPTs"
    
    def __str__(self):
        return f"IPT for {self.child.name} ({self.get_status_display()})"

class AdverseEvent(models.Model):
    child = models.ForeignKey(ChildProfile, on_delete=models.CASCADE, related_name='adverse_events')
    immunization = models.ForeignKey(
        Immunization, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='adverse_events'
    )
    date_occurred = models.DateField(default=timezone.now)
    description = models.TextField()
    vaccine_type = models.CharField(max_length=50, null=True, blank=True)
    batch_number = models.CharField(max_length=50, null=True, blank=True)
    manufacturer = models.CharField(max_length=100, null=True, blank=True)
    manufacture_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    action_taken = models.TextField(null=True, blank=True)
    reported_to_authorities = models.BooleanField(default=False)
    reported_date = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['-date_occurred']
        verbose_name = "Adverse Event Following Immunization"
        verbose_name_plural = "Adverse Events Following Immunization"
    
    def __str__(self):
        return f"AEFI for {self.child.name} on {self.date_occurred}"