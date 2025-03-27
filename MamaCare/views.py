
# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now

from .forms import AppointmentForm, ChildForm, ChildProfileForm, HealthRecordForm, MaternalProfileForm, MotherForm, PhysicalExaminationForm, PregnancyRecordForm, RecordForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, HospitalLoginForm, PreviousPregnancyForm
from .models import Appointment, Child, ChildProfile, HospitalUser, MaternalProfile, Mother, Patient, PreviousPregnancy
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
        # {"title": "ANC, Childbirth and Postnatal Care", "url": "anc_childbirth"},
        {"title": "Maternal Profile", "url": "maternal_profile_form"},
        {"title": "Child Profile", "url": "child_profile_form"},
        # {"title": "Medical & Surgical History", "url": "medical_history"},
        # {"title": "Previous Pregnancy", "url": "previous_pregnancy"},
        # {"title": "Physical Examination [1st Visit]", "url": "physical_exam"},
        # {"title": "Child Health Monitoring", "url": "child_health_monitoring"},
        # {"title": "Health Record of Child", "url": "health_record"},
        # {"title": "Immunization", "url": "immunization"},
        # {"title": "Family Planning", "url": "family_planning"},
        # {"title": "Hospital Admissions", "url": "hospital_admissions"},
    ]

    return render(request, 'add_new_record.html', {'form': form, 'sections': sections})




def child_profile_form(request):
    if request.method == "POST":
        form = ChildProfileForm(request.POST)
        if form.is_valid():
        # Save form or process data as needed
            form.save()
            return render(request, "success_page.html", {"message": "Child Profile Saved Successfully"})
    else:
        form = ChildProfileForm()
    return render(request, "child_profile_form.html", {"form": form})







def add_record(request):
    if request.method == "POST":
        mother_form = MotherForm(request.POST)
        child_form = ChildForm(request.POST)

        if mother_form.is_valid() and child_form.is_valid():
            mother = mother_form.save()
            child = child_form.save(commit=False)
            child.mother = mother
            child.save()
            return render(request, 'success.html', {'message': 'Record Added Successfully!'})

    else:
        mother_form = MotherForm()
        child_form = ChildForm()

    return render(request, 'add_mother_&_child_records.html', {'mother_form': mother_form, 'child_form': child_form})

def search_records(request):
    query = request.GET.get('q', '').strip()

    if query:
        # Search in Mother ID, Mother Name, or Child Name
        mothers = MaternalProfile.objects.filter(
            Q(mother_id__icontains=query) | 
            Q(mother_name__icontains=query) | 
            Q(childprofile__child_name__icontains=query)  # Related Child Profile
        ).distinct()

        # Prepare JSON response
        results = []
        for mother in mothers:
            child = ChildProfile.objects.filter(mother=mother).first()  # Get first child (if exists)
            results.append({
                "mother_id": mother.mother_id,
                "mother_name": mother.mother_name,
                "child_name": child.child_name if child else "No child record",
                "profile_url": f"/maternal_profile/{mother.mother_id}/"  # Link to profile
            })

        return JsonResponse(results, safe=False)

    return JsonResponse([], safe=False)
    return render(request, 'search_results.html', {'mothers': mothers, 'children': children})



def edit_record(request, mother_id):
    mother = get_object_or_404(Mother, id=mother_id)
    children = Child.objects.filter(mother=mother)

    if request.method == "POST":
        mother_form = MotherForm(request.POST, instance=mother)
        if mother_form.is_valid():
            mother_form.save()
            return render(request, 'success.html', {'message': 'Record Updated Successfully!'})

    else:
        mother_form = MotherForm(instance=mother)

        return render(request, 'edit_record.html', {'mother_form': mother_form, 'children': children})


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


def mother_detail(request, mother_id):
    mother = Mother.objects.get(id=mother_id)
    return render(request, 'mother_detail.html', {'mother': mother})

def child_detail(request, child_id):
    child = Child.objects.get(id=child_id)
    return render(request, 'child_detail.html', {'child': child})


def add_records(request):
    mother_form = MotherForm()
    child_form = ChildForm()
    health_record_form = HealthRecordForm()

    if request.method == "POST":
        mother_form = MotherForm(request.POST)
        child_form = ChildForm(request.POST)
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


def pregnancy_record_view(request):
    if request.method == 'POST':
        form = PregnancyRecordForm(request.POST)
        if form.is_valid():
            form.save()
            if 'redirect' in request.POST:
                return redirect('success_page')  # Replace with actual URL
            else:
                return redirect('pregnancy_record')  # Redirect back to form page

    else:
        form = PregnancyRecordForm()

    return render(request, 'pregnancy_record.html', {'form': form})


def update_existing_records(request):
    mother_name = None
    error_message = None  
    form_submitted = False  

    sections = [
        {"title": "Maternal Profile", "url": "maternal_profile_form"},
        {"title": "Child Profile", "url": "child_profile_form"},
    ]

    if request.method == "POST":  
        form_submitted = True  

        mother_id = request.POST.get("mother_id", "").strip()
        mother_name_input = request.POST.get("mother_name", "").strip()

        print(f"Searching for Mother ID: {mother_id}, Name: {mother_name_input}")  # Debug log

        if mother_id or mother_name_input:  
            try:
                if mother_id:
                        mother = MaternalProfile.objects.get(identification_number=mother_id)
                else:
                        mother = MaternalProfile.objects.get(name__icontains=mother_name_input)


                mother_name = mother.name  # Assign found mother's name
                print(f"Mother found: {mother_name}")  # Debug log
            except MaternalProfile.DoesNotExist:
                error_message = "Mother not found. Check the ID or name."
                print("Error: Mother not found!")  # Debug log
        else:
            error_message = "Please enter a Mother ID or Name."

    return render(request, "update_records.html", {
        "mother_name": mother_name,
        "sections": sections,
        "error_message": error_message if form_submitted else None,
        "form_submitted": form_submitted
    })