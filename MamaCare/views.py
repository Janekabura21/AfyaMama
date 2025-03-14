
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now

from .forms import AppointmentForm, MaternalProfileForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, HospitalLoginForm, PreviousPregnancyForm
from .models import Appointment, HospitalUser, MaternalProfile, Patient, PreviousPregnancy



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




# def maternal_profile_view(request, mother_id=None):  # Accept mother_id
#     if mother_id:
#         mother = get_object_or_404(MaternalProfile, id=mother_id)  # Get the mother's profile
#     else:
#         mother = None  # Allow creating a new maternal profile

#     if request.method == "POST":
#         form = MaternalProfileForm(request.POST, instance=mother)  # If editing, use instance
#         if form.is_valid():
#             mother = form.save()
#             messages.success(request, "Profile saved successfully!")
#             return redirect('maternal_profile', mother_id=mother.id)  # Redirect to profile page
#     else:
#         form = MaternalProfileForm(instance=mother)

#     return render(request, 'maternal_profile.html', {'form': form, 'mother': mother})

def maternal_profile_view(request):
    if request.method == "POST":
        form = MaternalProfileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile saved successfully!")
            return redirect('success_page')  # Ensure 'success_page' exists
    else:
        form = MaternalProfileForm()

    return render(request, 'maternal_profile_form.html', {'form': form})


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



def search_records(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    mothers = MaternalProfile.objects.filter(name__icontains=query) if query else []
    children = Patient.objects.filter(name__icontains=query) if query else []

    context = {
        'query': query,
        'mothers': mothers,
        'children': children,
    }
    return render(request, 'MamaCare/search_results.html', context)














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