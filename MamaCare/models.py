
from django.db import models
import uuid
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
    identification_number = models.CharField(max_length=20, null=True, blank=True)
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

    def save(self, *args, **kwargs):
        # If no ID is provided, generate a temporary one
        if not self.identification_number:
            self.identification_number = generate_temp_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.edd}"



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
    mother = models.ForeignKey(MaternalProfile, on_delete=models.CASCADE)
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
    


class Mother(models.Model):
    name = models.CharField(max_length=255)
    identification_number = models.CharField(max_length=20, unique=True)    
    medical_history = models.TextField()

    def __str__(self):
        return self.name

class Child(models.Model):
    mother = models.ForeignKey(Mother, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()

    health_record = models.ForeignKey(
        'HealthRecord',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="child_health_record")

    def __str__(self):
        
        return self.name





class HealthRecord(models.Model):
    mother = models.ForeignKey(Mother, on_delete=models.CASCADE, related_name="health_records", null=True, blank=True)
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name="health_records", null=True, blank=True)
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








class PregnancyRecord(models.Model):
    contact_number = models.PositiveIntegerField()
    date = models.DateField()
    urine = models.CharField(max_length=10, blank=True, null=True)
    muac = models.PositiveIntegerField(help_text="Mid Upper Arm Circumference (cm)")
    blood_pressure = models.CharField(max_length=10, help_text="e.g., 118/65 mmHg")
    hb = models.FloatField(help_text="Hemoglobin level (g/dl)")
    pallor = models.CharField(max_length=20, blank=True, null=True)
    gestation_weeks = models.PositiveIntegerField()
    fundal_height = models.CharField(max_length=10, blank=True, null=True)
    presentation = models.CharField(max_length=10, blank=True, null=True)
    lie = models.CharField(max_length=10, blank=True, null=True)
    fetal_heart_rate = models.PositiveIntegerField(help_text="Beats per minute")
    fetal_movement = models.BooleanField(default=True)
    mental_health_status = models.CharField(max_length=100, blank=True, null=True)
    next_visit = models.DateField()

    def __str__(self):
        return f"Pregnancy Record - {self.date} ({self.gestation_weeks} weeks)"







from django.db import models

class ChildProfile(models.Model):
    # A. Particulars of the Child
    name = models.CharField(max_length=100)
    sex = models.CharField(max_length=10, choices=[("Male", "Male"), ("Female", "Female")])
    date_of_birth = models.DateField()
    gestation_at_birth = models.PositiveIntegerField(null=True, blank=True)  # Weeks
    birth_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # in grams
    birth_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # in cm
    birth_order = models.PositiveIntegerField(null=True, blank=True)
    date_first_seen = models.DateField()

    # B. Health Record of Child
    place_of_birth = models.CharField(max_length=20, choices=[("Home", "Home"), ("Hospital", "Hospital"), ("Other", "Other")])
    health_facility_name = models.CharField(max_length=100, null=True, blank=True)
    birth_notification_no = models.CharField(max_length=20, null=True, blank=True)
    immunization_registration_no = models.CharField(max_length=20, null=True, blank=True)
    child_welfare_clinic_no = models.CharField(max_length=20, null=True, blank=True)
    master_facility_code = models.CharField(max_length=20, null=True, blank=True)

    # C. Civil Registration
    birth_certificate_no = models.CharField(max_length=20, null=True, blank=True)
    date_of_registration = models.DateField(null=True, blank=True)
    place_of_registration = models.CharField(max_length=100, null=True, blank=True)

    # D. Parent/Guardian Information
    fathers_name = models.CharField(max_length=100, null=True, blank=True)
    fathers_phone = models.CharField(max_length=20, null=True, blank=True)
    mothers_name = models.CharField(max_length=100)
    mothers_phone = models.CharField(max_length=20)
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

    def __str__(self):
        return self.name






















































