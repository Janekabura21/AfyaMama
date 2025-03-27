from django import views
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import  add_new_record, add_patient, add_previous_pregnancy, add_record, add_records, anc_childbirth_view, child_detail, child_health_monitoring_view, child_profile_form, edit_record, family_planning_view, health_record_view, hospital_admissions_view, hospital_dashboard, immunization_view, mark_attendance, maternal_profile_view, medical_history_view, mother_child_records, mother_detail, physical_exam_view, pregnancy_record_view, previous_pregnancy_list, previous_pregnancy_view, search_records, success_page, update_existing_records
from .views import register_hospital, login_hospital, update_appointment, delete_appointment, appointments_list



urlpatterns = [
    path('register/', register_hospital, name='register_hospital'),
    path('login/', login_hospital, name='login_hospital'),
    path('dashboard/', hospital_dashboard, name="hospital_dashboard"),
    path('add-patient/', add_patient, name='add_patient'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout_hospital'),
    path('success/', success_page, name='success_page'),
    path('appointment/update/<int:appointment_id>/<str:status>/', update_appointment, name='update_appointment'),
    path('appointment/delete/<int:appointment_id>/', delete_appointment, name='delete_appointment'),
    path('dashboard/appointments/', appointments_list, name='appointments_list'),
    path('appointment/mark-attendance/<int:appointment_id>/', mark_attendance, name='mark_attendance'),
    path('register/', register_hospital, name='register'),
    path('previous_pregnancies/', previous_pregnancy_list, name='previous_pregnancy_list'),
    path('add_previous_pregnancy/<int:mother_id>/', add_previous_pregnancy, name='add_previous_pregnancy'),
    path('search/', search_records, name='search_records'),
    path('dashboard/mother-child-records/', mother_child_records, name='mother_child_records'),
    # path('mother/<int:mother_id>/', mother_detail, name='mother_detail'),
    path('child/<int:child_id>/', child_detail, name='child_detail'),


    path('add-records/', add_record, name='add_record'),
    path('add_new_record/', add_new_record, name='add_new_record'),
    path('edit-record/<int:mother_id>/', edit_record, name='edit_record'),
    path('anc-childbirth/', anc_childbirth_view, name='anc_childbirth'),
    path('add_new_record/maternal-profile/', maternal_profile_view, name='maternal_profile_form'),
    path('medical-history/', medical_history_view, name='medical_history'),
    path('previous-pregnancy/', previous_pregnancy_view, name='previous_pregnancy'),
    path('physical-exam/', physical_exam_view, name='physical_exam'),
    path('child-health-monitoring/', child_health_monitoring_view, name='child_health_monitoring'),
    path('health-record/', health_record_view, name='health_record'),
    path('immunization/', immunization_view, name='immunization'),
    path('family-planning/', family_planning_view, name='family_planning'),
    path('hospital-admissions/', hospital_admissions_view, name='hospital_admissions'),
    path('pregnancy-record/', pregnancy_record_view, name='pregnancy_record'),
    path("child_profile_form/", child_profile_form, name="child_profile_form"),
    path("update_records/", update_existing_records, name="update_existing_records"),


    
    
]


# <int:mother_id>/