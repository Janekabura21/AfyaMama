from django import views
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import ( add_new_record, add_patient, add_previous_pregnancy,  add_records, anc_childbirth_view, 
                     child_health_monitoring_view, child_profile_form, edit_record, family_planning_view, 
                    health_record_view, hospital_admissions_view, hospital_dashboard, immunization_view, 
                    mark_attendance, maternal_profile_form, maternal_profile_view, medical_history_view, mother_child_records, new_child_profile_form, new_maternal_profile_form, 
                      search_records, success_page, update_existing_records, 
                    register_hospital, login_hospital, update_appointment, delete_appointment, appointments_list)

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
    
    path('add_previous_pregnancy/<str:mother_id>/', add_previous_pregnancy, name='add_previous_pregnancy'),
    path('search/', search_records, name='search_records'),
    path('dashboard/mother-child-records/', mother_child_records, name='mother_child_records'),
    
    path("edit-record/<str:mother_id>/", edit_record, name="edit_record"),


    path('add-records/', add_records, name='add_records'),
    path('add_new_record/', add_new_record, name='add_new_record'),


    path('new_child_profile_form/', new_child_profile_form, name='new_child_profile_form'),
    path('child_profile_form/<str:mother_id>/', child_profile_form, name='child_profile_form'),

    
    path('new_maternal-profile-form/', new_maternal_profile_form, name='new_maternal_profile_form'),  # New mother
    path('maternal-profile-form/<str:mother_id>/', maternal_profile_form, name='maternal_profile_form'),  # Edit existing mother




    path('anc-childbirth/<str:mother_id>/', anc_childbirth_view, name='anc_childbirth'),
    path('add_new_record/', maternal_profile_view, name='maternal_profile_form'),
    path('medical-history/<str:mother_id>/', medical_history_view, name='medical_history'),
    path('child-health-monitoring/<str:mother_id>/', child_health_monitoring_view, name='child_health_monitoring'),
    path('health-record/<str:mother_id>/', health_record_view, name='health_record'),
    path('immunization/<str:mother_id>/', immunization_view, name='immunization'),
    path('family-planning/<str:mother_id>/', family_planning_view, name='family_planning'),
    path('hospital-admissions/<str:mother_id>/', hospital_admissions_view, name='hospital_admissions'),
    
    path("update_records/", update_existing_records, name="update_existing_records"),



]






# maternal-profile/<int:mother_id>/























