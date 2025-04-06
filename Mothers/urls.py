# Mothers/urls.py

from django.urls import path
from .views import (register, setup_password)

app_name = 'Mothers'

urlpatterns = [
    path('register/', register, name='register'),
    path('setup-password/<str:identification_number>/', setup_password, name='setup_password'),
]
