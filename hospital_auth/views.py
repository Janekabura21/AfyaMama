

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import HospitalRegistrationForm, HospitalLoginForm
from .models import HospitalUser


def register_hospital(request):
    if request.method == "POST":
        form = HospitalRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('hospital_dashboard')  # Redirect to hospital dashboard after registration
    else:
        form = HospitalRegistrationForm()
    return render(request, 'hospital_auth/register.html', {'form': form})

def login_hospital(request):
    if request.method == "POST":
        form = HospitalLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('hospital_dashboard')  # Redirect to hospital dashboard after login
    else:
        form = HospitalLoginForm()
    return render(request, 'hospital_auth/login.html', {'form': form})

def logout_hospital(request):
    logout(request)
    return redirect('login_hospital')
