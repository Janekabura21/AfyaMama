from django import views
from django.urls import path
from .views import maternal_profile_view, success_page, health_facilities



urlpatterns = [
    path('home/', health_facilities, name='home'),
    path('maternal-profile/', maternal_profile_view, name='maternal_profile_form'),
    path('success/', success_page, name='success_page'),
]
