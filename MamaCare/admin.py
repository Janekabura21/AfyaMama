from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import HospitalUser, MaternalProfile, Patient, Appointment, PreviousPregnancy

# Customizing the HospitalUser Admin View
class HospitalUserAdmin(UserAdmin):
    ordering = ["email"]
    list_display = ["email", "hospital_name", "is_active"]
    list_filter = ["is_active"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("name",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "name", "password1", "password2", "is_active", "is_staff"),
        }),
    )

class PatientAdmin(admin.ModelAdmin):
    list_display = ("name", "hospital", "date_of_birth", "contact_number")
    search_fields = ("name", "hospital__hospital_name")

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "date", "status", "attended")
    search_fields = ("patient__name", "doctor__hospital_name")
    list_filter = ("status", "attended", "date")

class MaternalProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "gravida", "parity", "edd", "county", "telephone")
    search_fields = ("name", "id_number", "huduma_number", "telephone")
    list_filter = ("marital_status", "county", "education_level")

class PreviousPregnancyAdmin(admin.ModelAdmin):
    list_display = ('mother', 'pregnancy_order', 'year', 'mode_of_delivery', 'birth_weight', 'outcome')
    search_fields = ('mother__name', 'mode_of_delivery', 'outcome')

# ✅ Register models correctly
admin.site.register(HospitalUser, HospitalUserAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Appointment, AppointmentAdmin)  # ✅ Keep only this one
admin.site.register(MaternalProfile, MaternalProfileAdmin)
admin.site.register(PreviousPregnancy, PreviousPregnancyAdmin)












































