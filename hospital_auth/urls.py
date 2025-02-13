from django.urls import path
from .views import register_hospital, login_hospital, logout_hospital

urlpatterns = [
    path('register/', register_hospital, name='register_hospital'),
    path('login/', login_hospital, name='login_hospital'),
    path('logout/', logout_hospital, name='logout_hospital'),
]
