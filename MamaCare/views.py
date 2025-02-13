
# Create your views here.
from django.shortcuts import render, redirect
from .forms import MaternalProfileForm
from .models import HealthFacility 

from django.contrib import messages

def health_facilities(request):
    facilities = HealthFacility.objects.all()
    return render(request, 'health_facilities.html', {'facilities': facilities})

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
