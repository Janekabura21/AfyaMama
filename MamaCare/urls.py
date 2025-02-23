from django.urls import path
from django.contrib.auth import views as auth_views
from .views import hospital_dashboard, maternal_profile_view, success_page
from .views import register_hospital, login_hospital

urlpatterns = [
    path('register/', register_hospital, name='register_hospital'),
    path('login/', login_hospital, name='login_hospital'),
    path('dashboard/', hospital_dashboard, name="hospital_dashboard"),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout_hospital'),
    path('maternal-profile/', maternal_profile_view, name='maternal_profile_form'),
    path('success/', success_page, name='success_page'),
]
