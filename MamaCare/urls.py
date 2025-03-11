from django.urls import path
from django.contrib.auth import views as auth_views
from .views import add_patient, hospital_dashboard, mark_attendance, maternal_profile_view, success_page
from .views import register_hospital, login_hospital, update_appointment, delete_appointment, appointments_list

urlpatterns = [
    path('register/', register_hospital, name='register_hospital'),
    path('login/', login_hospital, name='login_hospital'),
    path('dashboard/', hospital_dashboard, name="hospital_dashboard"),
    path('add-patient/', add_patient, name='add_patient'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout_hospital'),
    path('maternal-profile/', maternal_profile_view, name='maternal_profile_form'),
    path('success/', success_page, name='success_page'),
    path('appointment/update/<int:appointment_id>/<str:status>/', update_appointment, name='update_appointment'),
    path('appointment/delete/<int:appointment_id>/', delete_appointment, name='delete_appointment'),
    path('dashboard/appointments/', appointments_list, name='appointments_list'),
    path('appointment/mark-attendance/<int:appointment_id>/', mark_attendance, name='mark_attendance'),
]


