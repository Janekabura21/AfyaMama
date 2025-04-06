# Mothers/views.py

from django.shortcuts import render, redirect
from .forms import MotherRegistrationForm
from MamaCare.models import MaternalProfile, HospitalUser

def register(request):
    error = None

    if request.method == 'POST':
        form = MotherRegistrationForm(request.POST)
        if form.is_valid():
            hospital_code = form.cleaned_data['hospital_code']
            hospital_name = form.cleaned_data['hospital_name']
            mother_name = form.cleaned_data['mother_name']
            identification_number = form.cleaned_data['identification_number']

            # Validate Hospital
            try:
                hospital = HospitalUser.objects.get(code=hospital_code, hospital_name=hospital_name)
            except HospitalUser.DoesNotExist:
                error = "Hospital not found. Please check the name and code."
                return render(request, 'mothers/register.html', {'form': form, 'error': error})

            # Validate Mother
            try:
                mother = MaternalProfile.objects.get(
                    identification_number=identification_number,
                    name=mother_name,
                    hospital=hospital
                )
                # Redirect to password setup
                return redirect('mothers:setup_password', identification_number=identification_number)

            except MaternalProfile.DoesNotExist:
                error = "You are not yet registered at the hospital. Please visit the hospital to complete registration."

    else:
        form = MotherRegistrationForm()

    return render(request, 'mothers/register.html', {'form': form, 'error': error})

def setup_password(request, identification_number):
    return render(request, 'mothers/setup_password.html', {'id': identification_number})

