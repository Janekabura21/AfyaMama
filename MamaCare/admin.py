from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import HospitalUser, MaternalProfile, Patient, Appointment

# Customizing the HospitalUser Admin View
class HospitalUserAdmin(UserAdmin):

    ordering = ["email"]  # ✅ Change from 'username' to 'email'
    list_display = ["email", "hospital_name", "is_active"]  # ✅ Remove 'username' and 'is_staff'
    list_filter = ["is_active"]  # ✅ Use 'is_active' instead of 'is_staff'

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



    # fieldsets = UserAdmin.fieldsets + (
    #     ("Hospital Details", {"fields": ("hospital_name", "code", "location", "contact_number")}),
    # )
    # list_display = ("username", "hospital_name", "code", "email", "is_staff", "is_active")
    # search_fields = ("username", "hospital_name", "email", "code")

# Register HospitalUser model
# admin.site.register(HospitalUser, HospitalUserAdmin)


# class HospitalUserAdmin(admin.ModelAdmin):
#     list_display = ("hospital_name", "username", "location", "contact_number")
#     search_fields = ("hospital_name", "username", "location")

# Customize Patient Admin Panel
class PatientAdmin(admin.ModelAdmin):
    list_display = ("name", "hospital", "date_of_birth", "contact_number")
    search_fields = ("name", "hospital__hospital_name")

# Customize Appointment Admin Panel
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "hospital", "date", "status")
    search_fields = ("patient__name", "hospital__hospital_name")
    list_filter = ("status", "date")

# Register models with their custom admin configurations
admin.site.register(HospitalUser, HospitalUserAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Appointment, AppointmentAdmin)

# Customizing the MaternalProfile Admin View
class MaternalProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "gravida", "parity", "edd", "county", "telephone")
    search_fields = ("name", "id_number", "huduma_number", "telephone")
    list_filter = ("marital_status", "county", "education_level")

# Register MaternalProfile model
admin.site.register(MaternalProfile, MaternalProfileAdmin)
