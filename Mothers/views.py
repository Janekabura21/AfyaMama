# Mothers/views.py

from django.shortcuts import get_object_or_404, render, redirect
from .forms import MotherRegistrationForm
from MamaCare.models import ChildProfile, MaternalProfile, HospitalUser
from .models import  MotherAccount
from MamaCare.models import Appointment

from .forms import MotherPasswordSetupForm
from MamaCare.models import HospitalUser
# views.py
from MamaCare.models import MaternalProfile  
from django.db.models import Q

def register(request):
    error = None

    if request.method == 'POST':
        form = MotherRegistrationForm(request.POST)
        if form.is_valid():
            hospital_code = form.cleaned_data['hospital_code'].strip()
            hospital_name = form.cleaned_data['hospital_name'].strip()
            mother_name = form.cleaned_data['mother_name'].strip()
            identification_number = form.cleaned_data['identification_number'].strip()

            # Validate Hospital
            try:
                hospital = HospitalUser.objects.get(
                    code__iexact=hospital_code,
                    hospital_name__iexact=hospital_name
                )
            except HospitalUser.DoesNotExist:
                error = "Hospital not found. Please check the hospital code and name."
                return render(request, 'mothers/register.html', {'form': form, 'error': error})

            # Validate Mother
            try:
                mother = MaternalProfile.objects.get(
                    identification_number=identification_number,
                    name__iexact=mother_name,
                    hospital=hospital
                )
                return redirect('mothers:setup_password', identification_number=identification_number)

            except MaternalProfile.DoesNotExist:
                error = (
                    "You are not yet registered at the hospital. "
                    "Please ensure your name and ID match exactly what was recorded during registration."
                )

    else:
        form = MotherRegistrationForm()

    return render(request, 'mothers/register.html', {'form': form, 'error': error})





def setup_password(request, identification_number):
    error = None
    success = None

    if request.method == 'POST':
        form = MotherPasswordSetupForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            id_number = form.cleaned_data['identification_number']
            password = form.cleaned_data['password']

            try:
                maternal_profile = MaternalProfile.objects.get(
                    identification_number=id_number,
                    name__iexact=name
                )

                # Check if already has a MotherAccount
                if MotherAccount.objects.filter(identification_number=id_number).exists():
                    error = "Account already set up. Please log in instead."
                else:
                    mother = MotherAccount(
                        identification_number=id_number,
                        name=name,
                    )
                    mother.set_password(password)
                    mother.save()
                    success = "Password setup successful. You can now log in."

            except MaternalProfile.DoesNotExist:
                error = "You are not registered at any hospital. Please register first."

    else:
        form = MotherPasswordSetupForm(initial={'identification_number': identification_number})

    return render(request, 'Mothers/setup_password.html', {'form': form, 'error': error, 'success': success})


def mothers_dashboard(request):
    """
    View to render the Mother's Dashboard after login.
    Displays links to maternal profile, appointments, notifications, and child records.
    """
    return render(request, 'Mothers/mothers_dashboard.html')


from django.shortcuts import render, get_object_or_404
from .models import MaternalProfile, ChildProfile, Appointment

def view_profile(request):
    # Get the maternal profile associated with the logged-in user
    mother = get_object_or_404(MaternalProfile, identification_number=request.user.email)

    # Count the children linked to this mother
    num_children = ChildProfile.objects.filter(mother=mother).count()

    # Upcoming appointments
    upcoming_appointments = Appointment.objects.filter(
        maternal_profile=mother,
        status='confirmed'
    ).order_by('date')[:3]

    context = {
        'mother': mother,
        'num_children': num_children,
        'upcoming_appointments': upcoming_appointments,
    }

    return render(request, 'Mothers/view_profile.html', context)
