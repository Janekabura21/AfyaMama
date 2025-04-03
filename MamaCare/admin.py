from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ChildProfile, HospitalUser, MaternalProfile, Patient, Appointment, PreviousPregnancy

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
    search_fields = ("name", "identification_number", "huduma_number", "telephone")
    list_filter = ("marital_status", "county", "education_level")

    def age(self, obj):
        # Calculate age based on date_of_birth field
        from datetime import date
        age = (date.today() - obj.date_of_birth).days // 365  # Age in years
        return age

    age.admin_order_field = 'date_of_birth'  # Enables sorting by date_of_birth
    age.short_description = "Age"


class PreviousPregnancyAdmin(admin.ModelAdmin):
    list_display = ('mother', 'pregnancy_order', 'year', 'mode_of_delivery', 'birth_weight', 'outcome')
    search_fields = ('mother__name', 'mode_of_delivery', 'outcome')


# In admin.py
@admin.register(ChildProfile)
class ChildProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'mothers_profile')
    list_display_links = ('id', 'name')










    from django.contrib import admin
from .models import Immunization, AdverseEvent

@admin.register(Immunization)
class ImmunizationAdmin(admin.ModelAdmin):
    list_display = ('get_mother_id', 'child_name', 'vaccine_type', 'date_administered', 'dose_number')
    list_filter = ('child__id', 'vaccine_type', 'date_administered')
    search_fields = ('child__id', 'child__name', 'vaccine_type')
    
    def get_mother_id(self, obj):
        return obj.child.id
    get_mother_id.short_description = 'Mother ID'
    get_mother_id.admin_order_field = 'child__id'
    
    def child_name(self, obj):
        return obj.child.name
    child_name.short_description = 'Child Name'

@admin.register(AdverseEvent)
class AdverseEventAdmin(admin.ModelAdmin):
    list_display = ('child', 'date_occurred', 'description', 'reported_to_authorities')
    list_filter = ('date_occurred', 'reported_to_authorities')
    search_fields = ('child__name', 'description', 'batch_number')


# ✅ Register models correctly
admin.site.register(HospitalUser, HospitalUserAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Appointment, AppointmentAdmin)  # ✅ Keep only this one
admin.site.register(MaternalProfile, MaternalProfileAdmin)
admin.site.register(PreviousPregnancy, PreviousPregnancyAdmin)












































