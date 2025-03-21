from django.urls import path
from django.contrib.auth import views as auth_views
from .views import  add_patient, add_previous_pregnancy, add_records, child_detail, hospital_dashboard, mark_attendance, maternal_profile_view, mother_child_records, mother_detail, previous_pregnancy_list, previous_pregnancy_view, search_records, success_page
from .views import register_hospital, login_hospital, update_appointment, delete_appointment, appointments_list
urlpatterns = [
    path('register/', register_hospital, name='register_hospital'),
    path('login/', login_hospital, name='login_hospital'),
    path('dashboard/', hospital_dashboard, name="hospital_dashboard"),
    path('add-patient/', add_patient, name='add_patient'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout_hospital'),
    path('dashboard/maternal-profile/', maternal_profile_view, name='maternal_profile_form'),
    path('success/', success_page, name='success_page'),
    path('appointment/update/<int:appointment_id>/<str:status>/', update_appointment, name='update_appointment'),
    path('appointment/delete/<int:appointment_id>/', delete_appointment, name='delete_appointment'),
    path('dashboard/appointments/', appointments_list, name='appointments_list'),
    path('appointment/mark-attendance/<int:appointment_id>/', mark_attendance, name='mark_attendance'),
    
    path('previous_pregnancies/', previous_pregnancy_list, name='previous_pregnancy_list'),
    path('add_previous_pregnancy/<int:mother_id>/', add_previous_pregnancy, name='add_previous_pregnancy'),
    path('search/', search_records, name='search_records'),
    path('dashboard/mother-child-records/', mother_child_records, name='mother_child_records'),
    path('mother/<int:mother_id>/', mother_detail, name='mother_detail'),
    path('child/<int:child_id>/', child_detail, name='child_detail'),
    path('add-records/', add_records, name='add_records'),
    # path('add-mother/', add_mother, name='add_mother'),
    # path('add-child/', add_child, name='add_child'),
    
]


# <int:mother_id>/