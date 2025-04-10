# Create your views here.
from asyncio import gather
from datetime import date, time, timezone
import datetime
import json
import random
from venv import logger
from django.forms import ValidationError
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import NoReverseMatch, reverse
from django.utils.timezone import now

from .forms import   ChildProfileForm, HealthRecordForm, HospitalLoginForm, HospitalRegistrationForm, HospitalUserForm, ImmunizationForm, MaternalProfileForm,  PhysicalExaminationForm,  RecordForm, SearchForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm,  PreviousPregnancyForm
from .models import  AntenatalVisit, ChildProfile, ChildWeightRecord,  HospitalUser, Immunization, LabTest, MaternalProfile, PreviousPregnancy 
from django.db.models import Q






from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator




# from .models import Mother, Child, BirthRecord, VaccinationRecord


otp_sent = False
otp_valid = False
sent_otp = None  # Store the OTP temporarily, this should be in session or cache for production.


def hospital_register(request):
    if request.method == "POST":
        form = HospitalUserForm(request.POST)

        if form.is_valid():
            # If the "Send OTP" button is clicked
            if 'send_notification' in request.POST:
                email = form.cleaned_data.get("email")
                
                # Generate and store OTP with timestamp
                otp = str(random.randint(100000, 999999))
                request.session['otp'] = otp
                request.session['otp_email'] = email
                request.session['otp_time'] = time.time()
                
                # Send OTP email
                try:
                    send_mail(
                        'Your OTP for Hospital Registration',
                        f'Your verification code is: {otp}\nThis code expires in 5 minutes.',
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=False,
                    )
                    messages.success(request, "OTP sent to your email address!")
                except Exception as e:
                    messages.error(request, f"Failed to send OTP: {str(e)}")
                    return redirect('hospital_register')
                
                return redirect('hospital_register')

            # If the "Submit Registration" button is clicked
            elif 'submit_registration' in request.POST:
                # Verify OTP
                user_otp = form.cleaned_data.get("otp")
                stored_otp = request.session.get('otp')
                otp_time = request.session.get('otp_time')
                
                # Check if OTP exists and is not expired (5 minutes)
                if not stored_otp or not otp_time:
                    messages.error(request, "Please request an OTP first")
                elif time.time() - otp_time > 300:  # 5 minutes expiry
                    messages.error(request, "OTP has expired. Please request a new one.")
                elif user_otp != stored_otp:
                    messages.error(request, "Invalid OTP. Please try again.")
                else:
                    # OTP is valid - complete registration
                    hospital_user = form.save(commit=False)
                    hospital_user.set_password(form.cleaned_data["password"])
                    hospital_user.save()
                    
                    # Clean up session
                    del request.session['otp']
                    del request.session['otp_email']
                    del request.session['otp_time']
                    
                    # Log the user in
                    login(request, hospital_user)
                    messages.success(request, "Registration successful!")
                    return redirect('hospital_dashboard')
        else:
            # Form is invalid
            messages.error(request, "Please correct the errors below.")
    else:
        form = HospitalUserForm()

    return render(request, 'register.html', {
        'form': form,
        'otp_sent': 'otp' in request.session
    })


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
     # Get hospital appointments
    
    context = {
        'hospital': hospital,
        
    }
    
    
    return render(request, "hospital_dashboard.html", context)

def logout_hospital(request):
    logout(request)
    return redirect('login_hospital')








def success_page(request):
    return render(request, 'success_page.html')

def add_patient(request):
    return render(request, 'add_patient.html')




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
        {"title": "Child Growth Chart", "url": "child_growth_chart"},
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


from django.shortcuts import render, redirect
from django.urls import reverse
from .models import MaternalProfile, ChildProfile

def update_existing_records(request):
    
    error_message = None

    if request.method == "POST":
        mother_id = request.POST.get("mother_id", "").strip()
        mother_name = request.POST.get("mother_name", "").strip()
        child_name = request.POST.get("child_name", "").strip()

        # 1️⃣ Enforce mandatory entry of either mother or child name
        if not mother_name and not child_name:
            error_message = "⚠️ Please enter at least the mother's name or child's name."
            return render(request, "update_records.html", {"error_message": error_message})

        print(f"🔍 Searching for: Mother ID: {mother_id}, Mother Name: {mother_name}, Child Name: {child_name}")

        mother = None
        child = None

        # 2️⃣ First, Search by Mother's ID (if provided)
        if mother_id:
            mother = MaternalProfile.objects.filter(identification_number=mother_id).first()
            if mother:
                return redirect(reverse("edit_record", args=[mother.identification_number]))

        # 3️⃣ If No ID, Search by Mother's Name (if provided)
        if not mother and mother_name:
            mother = MaternalProfile.objects.filter(name__icontains=mother_name).first()

        # 4️⃣ Search by Child's Name (if provided)
        if child_name:
            child = ChildProfile.objects.filter(name__icontains=child_name, mothers_profile__isnull=False).first()

        # 5️⃣ If Mother is Found, Redirect to Edit Record
        if mother:
            return redirect(reverse("edit_record", args=[mother.identification_number]))

        # 6️⃣ If Child is Found, Ensure They Have a Linked Mother Before Redirecting
        if child and child.mothers_profile:
            return redirect(reverse("edit_record", args=[child.mothers_profile.identification_number]))

        # 7️⃣ If No Valid Records Found, Show an Error
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
        "title": "Child Growth Chart",
        "url_name": "child_growth_chart",
        "data": children,  # assuming 'children' is a queryset of ChildProfile
        "type": "queryset"
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
            "title": "Immunization",
            "url_name": "immunization_view",
            "data": children,
            "type": "queryset"
        },
        {
            "title": "Antenatal, Lab & Weight Monitoring",
             "url_name": "maternal_monitoring",
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
            # If there is no data, still allow the section to be shown
            if not section["data"]:
                section["data"] = None  # Assigning None if no data exists

            # Always add section data to the list of processed sections
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











def child_profile_form(request, mother_id, child_id=None):  
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
                    
                    # Ensure mother's phone is set correctly
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
            if child_profile:
                # If editing, load existing data from the database
                form = ChildProfileForm(instance=child_profile)  
            else:
                # If new, pre-fill only mother's details
                initial_data = {
                'mother_id_number': maternal_profile.identification_number,
                'mothers_phone': maternal_profile.telephone,
            }
                form = ChildProfileForm(initial=initial_data)

        return render(request, 'child_profile_form.html', {
            'form': form,
            'mother_profile': maternal_profile,
            'is_new': is_new,
            'child_profile': child_profile  # Pass child data to the template
        })

    except MaternalProfile.DoesNotExist:
        messages.error(request, "Maternal profile not found.")
        return redirect('hospital_dashboard')

    except ChildProfile.DoesNotExist:
        messages.error(request, "Child profile not found.")
        return redirect('hospital_dashboard')

    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {str(e)}')
        return redirect('hospital_dashboard')  # Redirect to a safe page














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















from django.shortcuts import render, get_object_or_404, redirect
from .forms import ImmunizationForm
from .models import ChildProfile, Immunization
def immunization_view(request, child_id, immunization_id=None):
    # Fetch the child profile
    child = get_object_or_404(ChildProfile, id=child_id)

    # Access the mother's profile through the 'mothers_profile' field
    mother = child.mothers_profile

    # Fetch all immunization records for display (if needed)
    immunizations = Immunization.objects.filter(child=child)

    # If editing an existing immunization record
    if immunization_id:
        immunization = get_object_or_404(Immunization, id=immunization_id, child=child)
        form = ImmunizationForm(request.POST or None, instance=immunization)
    else:
        # Check if this child already has an immunization record
        immunization = Immunization.objects.filter(child=child).first()
        form = ImmunizationForm(request.POST or None, instance=immunization)

    if request.method == "POST":
        form = ImmunizationForm(request.POST, instance=immunization)
        if form.is_valid():
            immunization = form.save(commit=False)
            immunization.child = child  # Link the immunization to the child
            immunization.save()
            return redirect('immunization_view', child_id=child.id)

    # Render form page
    return render(request, "immunization_form.html", {
        "mother": mother,
        "child": child,
        "immunizations": immunizations,
        "form": form
    })

from django.utils import timezone


@login_required
def overview_view(request):
    # Get the hospital user
    hospital_user = HospitalUser.objects.get(email=request.user.email)
    print(f'Fetching data for hospital: {hospital_user.email}')

    # Count the maternal and child profiles linked to the hospital
    maternal_count = MaternalProfile.objects.filter(hospital=hospital_user).count()
    child_count = ChildProfile.objects.filter(mothers_profile__hospital=hospital_user).count()

    # Log the counts for debugging
    print(f'Maternal count: {maternal_count}')
    print(f'Child count: {child_count}')

    # Pass the counts to the template context
    context = {
        'registered_mothers': maternal_count,
        'registered_children': child_count,
    }

    return render(request, 'overview.html', context)




from django.shortcuts import render, get_object_or_404, redirect
import datetime
import calendar
from .models import ChildProfile, ChildWeightRecord, ChildHeightRecord
from django.shortcuts import render, get_object_or_404, redirect
import datetime
import calendar
import json
from django.core.serializers.json import DjangoJSONEncoder
from .models import ChildProfile, ChildWeightRecord, ChildHeightRecord

def child_growth_chart(request, child_id):
    child = get_object_or_404(ChildProfile, id=child_id)

    if request.method == 'POST':
        weight_kg = request.POST.get('weight_kg')
        height_cm = request.POST.get('height_cm')
        month = request.POST.get('month')
        age_group = request.POST.get('age_group')

        if weight_kg and month:
            ChildWeightRecord.objects.create(
                child=child,
                weight_kg=weight_kg,
                month=month,
                age_group=age_group
            )

        if height_cm and month:
            ChildHeightRecord.objects.create(
                child=child,
                height_cm=height_cm,
                month=month,
                age_group=age_group
            )

        return redirect('child_growth_chart', child_id=child.id)

    # Get all months from birth to current month
    birth_date = child.date_of_birth
    current_date = datetime.datetime.now().date()
    months_since_birth = (current_date.year - birth_date.year) * 12 + (current_date.month - birth_date.month)
    
    all_months = []
    for i in range(months_since_birth + 1):
        month_index = (birth_date.month - 1 + i) % 12
        year_offset = (birth_date.month - 1 + i) // 12
        month_label = f"{calendar.month_abbr[month_index + 1]} {birth_date.year + year_offset}"
        all_months.append(month_label)

    # Get all weight and height records ordered by month
    weight_records = ChildWeightRecord.objects.filter(child=child).order_by('month')
    height_records = ChildHeightRecord.objects.filter(child=child).order_by('month')

    # Create data arrays with None for missing months
    weight_data = {record.month: record.weight_kg for record in weight_records}
    height_data = {record.month: record.height_cm for record in height_records}
    
    weights = [weight_data.get(month) for month in all_months]
    heights = [height_data.get(month) for month in all_months]

    context = {
        'child': child,
        'months': all_months,
        'months_json': json.dumps(all_months, cls=DjangoJSONEncoder),
        'weights_json': json.dumps(weights, cls=DjangoJSONEncoder),
        'heights_json': json.dumps(heights, cls=DjangoJSONEncoder),
        'age_groups': [
            ("0-1", "0-1 years"),
            ("1-2", "1-2 years"), 
            ("2-3", "2-3 years"),
            ("3-4", "3-4 years"),
            ("4-5", "4-5 years")
        ]
    }

    return render(request, 'child_growth_chart.html', context)






from django.shortcuts import render, redirect
from .forms import AntenatalVisitForm, LabTestForm, WeightRecordForm
from .models import WeightRecord
from django.contrib import messages

def maternal_monitoring_view(request, mother_id):
    mother = get_object_or_404(MaternalProfile, identification_number=mother_id)

    antenatal_visits = AntenatalVisit.objects.filter(mother=mother).order_by('-visit_date')
    lab_tests = LabTest.objects.filter(mother=mother).order_by('-test_date')
    weight_records = WeightRecord.objects.filter(mother=mother).order_by('gestation_weeks')

    anc_form = AntenatalVisitForm()
    lab_form = LabTestForm()
    weight_form = WeightRecordForm()

    if request.method == 'POST':
        if 'save_anc' in request.POST:
            anc_form = AntenatalVisitForm(request.POST)
            if anc_form.is_valid():
                anc = anc_form.save(commit=False)
                anc.mother = mother
                anc.save()
                return redirect('maternal_monitoring', mother_id=mother_id)

        elif 'save_lab' in request.POST:
            lab_form = LabTestForm(request.POST)
            if lab_form.is_valid():
                lab = lab_form.save(commit=False)
                lab.mother = mother
                lab.save()
                return redirect('maternal_monitoring', mother_id=mother_id)

        elif 'save_weight' in request.POST:
            weight_form = WeightRecordForm(request.POST)
            if weight_form.is_valid():
                weight = weight_form.save(commit=False)
                weight.mother = mother
                weight.save()
                return redirect('maternal_monitoring', mother_id=mother_id)

    return render(request, 'maternal_monitoring.html', {
        'mother': mother,
        'antenatal_visits': antenatal_visits,
        'lab_tests': lab_tests,
        'weight_records': weight_records,
        'anc_form': anc_form,
        'lab_form': lab_form,
        'weight_form': weight_form,
    })


from django.shortcuts import render, get_object_or_404
from Mothers.models import MaternalProfile, ChildProfile

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import MaternalProfile, ChildProfile  # adjust to your app structure


def view_records_search(request):
    error_message = None

    if request.method == "POST":
        mother_id = request.POST.get("mother_id", "").strip()
        mother_name = request.POST.get("mother_name", "").strip()
        child_name = request.POST.get("child_name", "").strip()

        # Enforce mandatory entry
        if not mother_name and not child_name:
            error_message = "⚠️ Please enter at least the mother's name or child's name."
            return render(request, "view_records_search.html", {"error_message": error_message})

        # Search logic
        mother = None
        child = None

        if mother_id:
            mother = MaternalProfile.objects.filter(identification_number=mother_id).first()
            if mother:
                return redirect("view_records", mother_id=mother.identification_number)

        if not mother and mother_name:
            mothers = MaternalProfile.objects.filter(name__icontains=mother_name)
            if mothers.count() == 1:
                mother = mothers.first()

        if child_name:
            child = ChildProfile.objects.filter(
                name__icontains=child_name,
                mothers_profile__isnull=False
            ).first()

        # Determine redirect
        if mother:
            return redirect("view_records", mother_id=mother.identification_number)
        if child and child.mothers_profile:
            return redirect("view_records", mother_id=child.mothers_profile.identification_number)

        error_message = "❌ No matching records found. Please check the details and try again."

    return render(request, "view_records_search.html", {"error_message": error_message})

def view_records(request, mother_id):
    try:
        mother = get_object_or_404(MaternalProfile, identification_number=mother_id)
        children = ChildProfile.objects.filter(mothers_profile=mother)
        
        # GET parameters for additional filtering
        child_name = request.GET.get('child_name', '')
        if child_name:
            children = children.filter(name__icontains=child_name)

        sections = [
            {"title": "Child Growth Chart", "url_name": "child_growth_chart"},
            {"title": "Maternal Profile", "url_name": "maternal_profile_form"},
            {"title": "Child Profile", "url_name": "child_profile_form"},
            {"title": "Immunization", "url_name": "immunization_view"},
            {"title": "Antenatal Monitoring", "url_name": "maternal_monitoring"},
        ]

        processed_sections = []
        for section in sections:
            try:
                processed_sections.append({
                    "title": section["title"],
                    "url": reverse(section["url_name"], args=[mother.identification_number])
                })
            except Exception as e:
                print(f"Section error: {e}")

        return render(request, "view_records.html", {
            "mother": mother,
            "children": children,
            "sections": processed_sections,
            "mother_id": mother.identification_number  # Explicitly pass for template
        })

    except Exception as e:
        print(f"Error in view_records: {e}")
        return render(request, "view_records.html", {"error": str(e)})