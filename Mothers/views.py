from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MaternalProfile, Appointment, Notification

@login_required
def book_appointment(request):
    """Allow mothers to book appointments"""
    from .forms import AppointmentForm 

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.mother = request.user.maternalprofile  # Link to mother
            appointment.save()
            messages.success(request, "Appointment booked successfully!")
            return redirect('appointments_list')
    else:
        form = AppointmentForm()
    
    return render(request, 'Mothers/book_appointment.html', {'form': form})

@login_required
def update_maternal_profile(request):
    """Allow mothers to update their maternal profile"""
    from .forms import  MaternalProfileForm


    profile = get_object_or_404(MaternalProfile, user=request.user)

    if request.method == 'POST':
        form = MaternalProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('maternal_profile')
    else:
        form = MaternalProfileForm(instance=profile)

    return render(request, 'Mothers/update_profile.html', {'form': form})


@login_required
def notifications(request):
    """Display notifications for the logged-in mother."""
    user_notifications = Notification.objects.filter(mother__user=request.user).order_by('-created_at')

    return render(request, 'Mothers/notifications.html', {'notifications': user_notifications})


@login_required
def maternal_profile(request):
    """Display the maternal profile of the logged-in mother."""
    profile = get_object_or_404(MaternalProfile, user=request.user)
    return render(request, 'Mothers/maternal_profile.html', {'profile': profile})
