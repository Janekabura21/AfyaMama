
# Create your views here.
from django.shortcuts import render, redirect
from .forms import MaternalProfileForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, HospitalLoginForm
from .models import HospitalUser, Patient, Appointment




# def register_hospital(request):
#     print("DEBUG: View function called!")  # Check if the function is executed
    
#     if request.method == "POST":
#         form = HospitalRegistrationForm(request.POST)
#         if form.is_valid():
#             print("DEBUG: Form is valid!")
#             user = form.save()
#             login(request, user)
#             return redirect('hospital_dashboard')
#         else:
#             print("DEBUG: Form errors:", form.errors)

#     else:
#         print("DEBUG: Rendering registration form")  
#         form = HospitalRegistrationForm()

#     return render(request, "afya_mama/register.html", {"form": form})


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
            email = form.cleaned_data['username']
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


# def login_hospital(request):
#     if request.method == "POST":
#         form = HospitalLoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('hospital_dashboard')  # Redirect to hospital dashboard after login
#     else:
#         form = HospitalLoginForm()
#     return render(request, 'login.html', {'form': form})


@login_required
def hospital_dashboard(request):
    hospital = HospitalUser.objects.get(username=request.user.username)  # Assuming each hospital has a user account
    total_patients = Patient.objects.filter(hospital=hospital).count()
    upcoming_appointments = Appointment.objects.filter(hospital=hospital, status="Upcoming").count()

    context = {
        "hospital": hospital,
        "total_patients": total_patients,
        "upcoming_appointments": upcoming_appointments,
    }
    
    return render(request, "hospital_dashboard.html", context)

def logout_hospital(request):
    logout(request)
    return redirect('login_hospital')


def maternal_profile_view(request):
    if request.method == "POST":
        form = MaternalProfileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile saved successfully!")
            return redirect('maternal_profile_form')  # Redirect to the same form page
    else:
        form = MaternalProfileForm()

    return render(request, 'maternal_profile_form.html', {'form': form})

def success_page(request):
    return render(request, 'success_page.html')



















# def maternal_profile_view(request):
#     if request.method == "POST":
#         form = MaternalProfileForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('success_page')  # Redirect to success page
#     else:
#         form = MaternalProfileForm()

#     return render(request, 'maternal_profile_form.html', {'form': form})
