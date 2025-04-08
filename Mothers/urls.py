# Mothers/urls.py

from django.urls import path
from .views import (mothers_dashboard, register, setup_password, view_profile)

app_name = 'mothers'

urlpatterns = [
    path('register/', register, name='register'),
    path('setup-password/<str:identification_number>/', setup_password, name='setup_password'),
    path('dashboard/', mothers_dashboard, name='dashboard'),
    path('profile/', view_profile, name='view_profile'),
    # path('appointments/', view_appointments, name='view_appointments'),
    # path('notifications/', notifications, name='notifications'),
    # path('child-records/', child_records, name='child_records'),
]

