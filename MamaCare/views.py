# Create your views here.
from datetime import date, timezone
import datetime
from venv import logger
from django.forms import ValidationError
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import NoReverseMatch, reverse
from django.utils.timezone import now

from .forms import AppointmentForm,  ChildProfileForm, HealthRecordForm, ImmunizationForm, MaternalProfileForm,  PhysicalExaminationForm,  RecordForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, HospitalLoginForm, PreviousPregnancyForm
from .models import Appointment, ChildProfile, HospitalUser, Immunization, MaternalProfile, PreviousPregnancy 
from django.db.models import Q



# from .models import Mother, Child, BirthRecord, VaccinationRecord


def register_hospital(request):

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('hospital_dashboard')  # Redirect to hospital dashboard after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_hospital(request):
    if request.method == "POST":
        form = HospitalLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)  # Use email for authentication
            if user is not None:
                login(request, user)
                return redirect('hospital_dashboard')
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = HospitalLoginForm()

    return render(request, 'login.html', {'form': form})



@login_required
def hospital_dashboard(request):
    # hospital = request.user
    hospital = get_object_or_404(HospitalUser, email=request.user.email)  # Get the logged-in hospital user
    appointments = Appointment.objects.filter(hospital=hospital).order_by('-date')  # Get hospital appointments
    
    context = {
        'hospital': hospital,
        'appointments': appointments,
    }
    
    
    return render(request, "hospital_dashboard.html", context)

def logout_hospital(request):
    logout(request)
    return redirect('login_hospital')








def success_page(request):
    return render(request, 'success_page.html')

def add_patient(request):
    return render(request, 'add_patient.html')

@login_required
def update_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect("hospital_dashboard")
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, "update_appointment.html", {"form": form})

@login_required
def delete_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    if request.method == "POST":
        appointment.delete()
        return redirect("hospital_dashboard")
    return render(request, "delete_appointment.html", {"appointment": appointment})




def appointments_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'appointments_list.html', {'appointments': appointments})






def add_new_record(request):
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to the dashboard after saving
    else:
        form = RecordForm()

    sections = [
        
        {"title": "Maternal Profile", "url": "new_maternal_profile_form"},
        {"title": "Child Profile", "url": "new_child_profile_form"},
    ]

    return render(request, 'add_new_record.html', {'form': form, 'sections': sections})




def search_records(request):
    results = []
    error_message = ""

    if request.method == "GET":
        # Get the search parameters from the request
        mother_name = request.GET.get("mother_name", "").strip()
        mother_identification = request.GET.get("mother_identification", "").strip()
        child_name = request.GET.get("child_name", "").strip()

        if mother_identification:
            # Search for mother by identification number (ID or birth certificate)
            try:
                mother = MaternalProfile.objects.get(identification_number=mother_identification)
                # Also search for the child linked to that mother
                child = ChildProfile.objects.filter(mothers_profile=mother)
                results.append({"mother": mother, "children": child})
            except MaternalProfile.DoesNotExist:
                error_message = "No mother found with that identification number."
        
        elif mother_name:
            # Search for mothers by name
            mothers = MaternalProfile.objects.filter(name__icontains=mother_name)
            if mothers.exists():
                for mother in mothers:
                    # For each mother, fetch linked children
                    children = ChildProfile.objects.filter(mothers_profile=mother)
                    results.append({"mother": mother, "children": children})
            else:
                error_message = "No mothers found with that name."
        
        elif child_name:
            # Search for children by name and return the corresponding mother
            children = ChildProfile.objects.filter(name__icontains=child_name)
            if children.exists():
                for child in children:
                    mother = child.mothers_profile
                    results.append({"mother": mother, "children": [child]})
            else:
                error_message = "No children found with that name."
        
        else:
            error_message = "Please enter search criteria."

        # If no records were found, show the error message
        if not results:
            error_message = error_message or "No records match the entered criteria."

    return render(request, "search_records.html", {
        "results": results,
        "error_message": error_message
    })


def mother_child_records(request):
    sections = [
        {"title": "ANC, Childbirth and Postnatal Care", "url": "anc_childbirth"},
        {"title": "Maternal Profile", "url": "maternal_profile"},
        {"title": "Medical & Surgical History", "url": "medical_history"},
        {"title": "Previous Pregnancy", "url": "previous_pregnancy"},
        {"title": "Physical Examination [1st Visit]", "url": "physical_exam"},
        {"title": "Child Health Monitoring", "url": "child_health_monitoring"},
        {"title": "Health Record of Child", "url": "health_record"},
        {"title": "Immunization", "url": "immunization"},
        {"title": "Family Planning", "url": "family_planning"},
        {"title": "Hospital Admissions", "url": "hospital_admissions"},
    ]
    return render(request, "view_records.html", {"sections": sections})


# def mother_detail(request, mother_id):
#     mother = Mother.objects.get(id=mother_id)
#     return render(request, 'mother_detail.html', {'mother': mother})

# def child_detail(request, child_id):
#     child = Child.objects.get(id=child_id)
#     return render(request, 'child_detail.html', {'child': child}


def add_records(request):
    mother_form = MaternalProfileForm()
    child_form = ChildProfileForm()
    health_record_form = HealthRecordForm()

    if request.method == "POST":
        mother_form = MaternalProfileForm(request.POST)
        child_form = ChildProfileForm(request.POST)
        health_record_form = HealthRecordForm(request.POST)

        if mother_form.is_valid():
            mother_form.save()
        if child_form.is_valid():
            child_form.save()
        if health_record_form.is_valid():
            health_record_form.save()

    return render(request, "add_mother_&_child_records.html", {
        "mother_form": mother_form,
        "child_form": child_form,
        "health_record_form": health_record_form
    })










@login_required
def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'hospital/appointments.html', {'appointments': appointments})

@login_required
def update_appointment_status(request, appointment_id, status):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = status
    appointment.save()
    return redirect('appointment_list')

@login_required
def mark_attendance(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.attended = True
    appointment.save()
    return redirect('appointment_list')


def previous_pregnancy_view(request, mother_id):
    mother = get_object_or_404(MaternalProfile, id=mother_id)
    pregnancies = PreviousPregnancy.objects.filter(mother=mother)

    return render(request, "previous_pregnancy.html", {"mother": mother, "pregnancies": pregnancies})


def previous_pregnancy_list(request):
    pregnancies = PreviousPregnancy.objects.all()
    return render(request, 'previous_pregnancy_list.html', {'pregnancies': pregnancies})

def add_previous_pregnancy(request, mother_id):
    mother = get_object_or_404(MaternalProfile, id=mother_id)
    
    if request.method == "POST":
        form = PreviousPregnancyForm(request.POST)
        if form.is_valid():
            pregnancy = form.save(commit=False)
            pregnancy.mother = mother
            pregnancy.save()
            return redirect('previous_pregnancy_list')  # Redirect to the pregnancy list page

    else:
        form = PreviousPregnancyForm()

    return render(request, 'add_previous_pregnancy.html', {'form': form, 'mother': mother})



def update_existing_records(request):
    error_message = None

    if request.method == "POST":
        mother_id = request.POST.get("mother_id", "").strip()
        mother_name = request.POST.get("mother_name", "").strip()
        child_name = request.POST.get("child_name", "").strip()

        print(f"🔍 Searching for: Mother ID: {mother_id}, Mother Name: {mother_name}, Child Name: {child_name}")

        mother = None
        child = None

        # 1️⃣ First, Search by Identification Number (Highest Priority)
        if mother_id:
            mother = MaternalProfile.objects.filter(identification_number=mother_id).first()
            child = ChildProfile.objects.filter(id=mother_id).first()  # Find child with same ID

        # 2️⃣ If No ID was provided, Search by Name
        if not mother and mother_name:
            mother = MaternalProfile.objects.filter(name__icontains=mother_name).first()
        if not child and child_name:
            child = ChildProfile.objects.filter(name__icontains=child_name).first()

        # 3️⃣ If Mother is Found, Redirect to Edit Record
        if mother:
            return redirect(reverse("edit_record", args=[mother.identification_number]))

        # 4️⃣ If Child is Found but No Mother was Entered, Use Child’s Mother
        if child and child.mothers_profile:
            return redirect(reverse("edit_record", args=[child.mothers_profile.identification_number]))

        # 5️⃣ If No Records Found, Show an Error
        error_message = "❌ No matching records found. Please check the details and try again."

    return render(request, "update_records.html", {"error_message": error_message})











def anc_childbirth_view(request):
    return render(request, 'anc_childbirth.html')

def maternal_profile_view(request):
    if request.method == "POST":
        form = MaternalProfileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile saved successfully!")
            return redirect('success_page') 
    else:
        form = MaternalProfileForm()

    return render(request, 'maternal_profile_form.html', {'form': form})


def medical_history_view(request):
    return render(request, 'medical_history.html')

def previous_pregnancy_view(request):
    return render(request, 'previous_pregnancy.html')

def physical_exam_view(request):


    if request.method == "POST":
        form = PhysicalExaminationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Redirect to a success page
    else:
        form = PhysicalExaminationForm()
    
    return render(request, 'physical_examination.html', {'form': form})

    

def child_health_monitoring_view(request):
    return render(request, 'child_health_monitoring.html')

def health_record_view(request):
    return render(request, 'health_record.html')

def immunization_view(request):
    return render(request, 'immunization.html')

def family_planning_view(request):
    return render(request, 'family_planning.html')

def hospital_admissions_view(request):
    return render(request, 'hospital_admissions.html')











from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import MaternalProfile, ChildProfile

def edit_record(request, mother_id):
    # Get mother by identification_number
    mother = get_object_or_404(MaternalProfile, identification_number=mother_id)
    
    # Get children
    
    children = ChildProfile.objects.filter(mothers_profile=mother)
    
    # children = ChildProfile.objects.filter(
    #     id=mother.identification_number,
    #     mothers_profile=mother)

    # Define sections
    sections = [
        {
            "title": "ANC, Childbirth and Postnatal Care",
            "url_name": "anc_childbirth",
            "data": mother,
            "type": "single"
        },
        {
            "title": "Maternal Profile",
            "url_name": "maternal_profile_form", 
            "data": mother,
            "type": "single"
        },
        {
            "title": "Child Profile",
            "url_name": "child_profile_form", 
            "data": children,
            "type": "queryset"
        },
        {
            "title": "Medical & Surgical History",
            "url_name": "medical_history",
            "data": mother,
            "type": "single"
        },
        {
            "title": "Child Health Monitoring",
            "url_name": "child_health_monitoring",
            "data": children,
            "type": "queryset"
        },
        {
            "title": "Health Record of Child",
            "url_name": "health_record",
            "data": children,
            "type": "queryset"
        },
        {
            "title": "Immunization",
            "url_name": "immunization",
            "data": children,
            "type": "queryset"
        },
        {
            "title": "Family Planning",
            "url_name": "family_planning",
            "data": mother,
            "type": "single"
        },
        {
            "title": "Hospital Admissions",
            "url_name": "hospital_admissions",
            "data": mother,
            "type": "single"
        },
    ]

    # Process sections correctly
    processed_sections = []
    for section in sections:
        try:
            section_data = {
                "title": section["title"],
                "url": reverse(section["url_name"], args=[mother.identification_number])
            }
            processed_sections.append(section_data)
        except Exception as e:
            print(f"Error processing section {section['title']}: {e}")

    return render(request, "edit_record.html", {
        "mother": mother,
        "children": children,
        "sections": processed_sections
         
    })

























# from django.urls import reverse

# def edit_record(request, mother_id):
    
#         # Get mother by identification_number
#         mother = get_object_or_404(MaternalProfile, identification_number=mother_id)
        
#         # Get children - using both filters for reliability
#         children = ChildProfile.objects.filter(
#         id=mother.identification_number,
#         mothers_profile=mother
#     )

#     # Define ALL fields you want to include
#         child_fields = [
#         'id', 'name', 'sex', 'date_of_birth', 'gestation_at_birth',
#         'birth_weight', 'birth_length', 'birth_order', 'date_first_seen',
#         'place_of_birth', 'health_facility_name', 'birth_notification_no',
#         'immunization_registration_no', 'child_welfare_clinic_no',
#         'master_facility_code', 'birth_certificate_no', 'date_of_registration',
#         'place_of_registration', 'fathers_name', 'fathers_phone',
#         'mothers_phone', 'guardian_name', 'guardian_phone', 'residence',
#         'county', 'division', 'sub_county', 'town', 'estate_village',
#         'postal_address'
#     ]


#         sections = [
#             {
#                 "title": "ANC, Childbirth and Postnatal Care",
#                 "url_name": "anc_childbirth",
#                 "data": mother,
#                 "type": "single"
#             },
#             {
#                 "title": "Maternal Profile",
#                 "url_name": "maternal_profile_form", 
#                 "data": mother,
#                 "type": "single"
#             },
#             {
#                 "title": "Child Profile",
#                 "url_name": "child_profile_form",
#                 "data": children,
#                 "type": child_fields
#             },
#             {
#                 "title": "Medical & Surgical History",
#                 "url_name": "medical_history",
#                 "data": mother,
#                 "type": "single"
#             },
#             {
#                 "title": "Child Health Monitoring",
#                 "url_name": "child_health_monitoring",
#                 "data": children,
#                 "type": "queryset"
#             },
#             {
#                 "title": "Health Record of Child",
#                 "url_name": "health_record",
#                 "data": children,
#                 "type": "queryset"
#             },
#             {
#                 "title": "Immunization",
#                 "url_name": "immunization",
#                 "data": children,
#                 "type": "queryset"
#             },
#             {
#                 "title": "Family Planning",
#                 "url_name": "family_planning",
#                 "data": mother,
#                 "type": "single"
#             },
#             {
#                 "title": "Hospital Admissions",
#                 "url_name": "hospital_admissions",
#                 "data": mother,
#                 "type": "single"
#             },
#         ]

#         # Prepare data for template
#         processed_sections = []
#         for section in sections:
#             section_data = {
#             "title": section["title"],
#             "url": reverse(section["url_name"], args=[mother.identification_number]),
#         }

#         if section["type"] == "queryset":
#             section_data["data"] = []
#             for child in section["data"]:
#                 child_data = {}
#                 for field in section.get("fields", []):
#                     # Handle special cases
#                     if field == 'sex':
#                         child_data[field] = child.get_sex_display()
#                     else:
#                         value = getattr(child, field, None)
#                         # Format dates properly
#                         if value and field.endswith('_date') or field.endswith('_birth'):
#                             value = value.strftime("%m/%d/%Y")
#                         child_data[field] = value
#                 section_data["data"].append(child_data)

#         processed_sections.append(section_data)

#         return render(request, "edit_record.html", {
#         "mother": mother,
#         "children": children,
#         "sections": processed_sections,
#         "all_child_fields": child_fields  # Pass field list to template
#         })


def maternal_profile_form(request, mother_id=None):
    if mother_id:
        # Change from id=mother_id to identification_number=mother_id
        mother = get_object_or_404(MaternalProfile, identification_number=mother_id)
    else:
        mother = None  # No mother exists yet

    if request.method == "POST":
        form = MaternalProfileForm(request.POST, instance=mother)
        if form.is_valid():
            mother = form.save()
            return redirect('edit_record', mother_id=mother.identification_number)
    else:
        form = MaternalProfileForm(instance=mother)

    return render(request, "maternal_profile_form.html", {
        "form": form, 
        "mother": mother
    })











def child_profile_form(request, mother_id, child_id=None):  # 🔥 Allow editing existing child records
    try:
        # Get the maternal profile using `identification_number`
        maternal_profile = get_object_or_404(MaternalProfile, identification_number=mother_id)

        # Check if editing an existing child profile
        if child_id:
            child_profile = get_object_or_404(ChildProfile, id=child_id, mothers_profile=maternal_profile)  # ✅ Fetch existing child
            is_new = False
        else:
            child_profile = None
            is_new = True  # New child profile

        if request.method == 'POST':
            form = ChildProfileForm(request.POST, instance=child_profile)  # ✅ Use instance for updating
            if form.is_valid():
                try:
                    child_profile = form.save(commit=False)
                    child_profile.mothers_profile = maternal_profile
                    child_profile.mother_id_number = maternal_profile.identification_number
                    
                    # Set default values if needed
                    if not child_profile.mothers_phone:
                        child_profile.mothers_phone = maternal_profile.telephone
                    
                    child_profile.save()
                    messages.success(request, 'Child profile saved successfully!')
                    return redirect('edit_record', mother_id=maternal_profile.identification_number)
                
                except Exception as e:
                    messages.error(request, f'Error saving child profile: {str(e)}')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            # If editing, load existing data; otherwise, load default values
            initial_data = {
                'mother_id_number': maternal_profile.identification_number,
                'mothers_phone': maternal_profile.telephone,
            }
            form = ChildProfileForm(instance=child_profile, initial=initial_data)  # ✅ Pre-fill form

        return render(request, 'child_profile_form.html', {
            'form': form,
            'mother_profile': maternal_profile,
            'is_new': is_new,
            'child_profile': child_profile  # Pass child data to the template
        })

    except Exception as e:
        messages.error(request, 'An unexpected error occurred.')
        return redirect('hospital_dashboard')  # Redirect to a safe page

























# def child_profile_form(request, mother_id):
#     try:
#         # Use identification_number instead of id
#         maternal_profile = get_object_or_404(MaternalProfile, identification_number=mother_id)
        
#         if request.method == 'POST':
#             form = ChildProfileForm(request.POST)
#             if form.is_valid():
#                 try:
#                     child_profile = form.save(commit=False)
#                     child_profile.mothers_profile = maternal_profile
#                     child_profile.mother_id_number = maternal_profile.identification_number
                    
#                     # Set default values if needed
#                     if not child_profile.mothers_phone:
#                         child_profile.mothers_phone = maternal_profile.telephone
                    
#                     child_profile.save()
#                     messages.success(request, 'Child profile saved successfully!')
#                     return redirect('edit_record', mother_id=maternal_profile.identification_number)
                
#                 except Exception as e:
#                     messages.error(request, f'Error saving child profile: {str(e)}')
#             else:
#                 messages.error(request, 'Please correct the errors below.')
#         else:
#             initial_data = {
#                 'mother_id_number': maternal_profile.identification_number,
#                 'mothers_phone': maternal_profile.telephone,
#             }
#             form = ChildProfileForm(initial=initial_data)

#         return render(request, 'child_profile_form.html', {
#             'form': form,
#             'mother_profile': maternal_profile,
#             'is_new': True
#         })

#     except Exception as e:
#         messages.error(request, 'An unexpected error occurred.')
#         return redirect('hospital_dashboard')  # Redirect to a safe page










def new_maternal_profile_form(request):
    if request.method == 'POST':
        form = MaternalProfileForm(request.POST)
        if form.is_valid():
            try:
                maternal_profile = form.save()  # Changed from save(commit=False) to save()
                
                messages.success(request, "Profile created successfully!")
                return redirect('success_page')  # Explicit simple redirect
                
            except ValidationError as e:
                form.add_error(None, str(e))
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, "System error occurred. Please try again.")
                logger.error(f"Profile creation error: {e}")
    else:
        form = MaternalProfileForm()

    return render(request, 'new_maternal_profile_form.html', {
        'form': form,
        'is_new': True,
        'form_action': reverse('new_maternal_profile_form')  # Explicit form action
    })


def new_child_profile_form(request):
    if request.method == 'POST':
        form = ChildProfileForm(request.POST)
        if form.is_valid():
            try:
                # Save the form and get the child instance
                child_profile = form.save()  # Changed variable name
                
                messages.success(request, "Child profile created successfully!")
                return redirect('success_page')
                
            except ValidationError as e:
                form.add_error(None, str(e))
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, "System error occurred. Please try again.")
                logger.error(f"Profile creation error: {e}")
    else:
        form = ChildProfileForm()

    return render(request, 'new_child_profile_form.html', {
        'form': form,
        'is_new': True,
        'form_action': reverse('new_child_profile_form')
    })














# def update_existing_records(request):
#     error_message = None
#     search_results = []

#     if request.method == "POST":
#         mother_id = request.POST.get("mother_id", "").strip()
#         mother_name = request.POST.get("mother_name", "").strip()
#         child_name = request.POST.get("child_name", "").strip()

#         print(f"🔍 Searching for: Mother ID: {mother_id}, Mother Name: {mother_name}, Child Name: {child_name}")

#         # Check for matching records
#         mother = None
#         child = None

#         if mother_id:
#             mother = MaternalProfile.objects.filter(identification_number=mother_id).first()
#         elif mother_name:
#             mother = MaternalProfile.objects.filter(name__icontains=mother_name).first()

#         if child_name:
#             child = ChildProfile.objects.filter(name__icontains=child_name).first()

#         # If a mother is found, use her ID
#         if mother:
#             return redirect(reverse("edit_record", args=[mother.identification_number]))

#         # If a child is found but no mother was provided, use the child's linked mother
#         if child and child.mothers_profile:
#             return redirect(reverse("edit_record", args=[child.mothers_profile.identification_number]))

#         # No records found
#         error_message = "❌ No matching records found. Please check the details and try again."

#     return render(request, "update_records.html", {"error_message": error_message})






def immunization_view(request, mother_id):
    mother = get_object_or_404(MaternalProfile, identification_number=mother_id)
    children = ChildProfile.objects.filter(mothers_profile=mother)
    immunizations = Immunization.objects.filter(child__in=children).order_by('date_administered')

    # Handle form submission
    if request.method == "POST":
        form = ImmunizationForm(request.POST)
        if form.is_valid():
            immunization = form.save(commit=False)
            immunization.save()
            messages.success(request, "Immunization record added successfully.")
            return redirect('success_page', mother_id=mother.identification_number)  # Refresh page
    else:
        form = ImmunizationForm()  # Empty form if GET request

    return render(request, "immunization_form.html", {
        "mother": mother,
        "children": children,
        "immunizations": immunizations,
        "form": form,  # Pass form to template
    })