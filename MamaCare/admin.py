from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ChildProfile, HospitalUser, Immunization, MaternalProfile,  PreviousPregnancy
from datetime import date

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



class MaternalProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "gravida", "parity", "edd", "county", "telephone")
    search_fields = ("name", "identification_number", "huduma_number", "telephone")
    list_filter = ("marital_status", "county", "education_level")

    def age(self, obj):
        if obj.date_of_birth:
            return (date.today() - obj.date_of_birth).days // 365
        return None
    age.admin_order_field = 'date_of_birth'
    age.short_description = "Age"

class PreviousPregnancyAdmin(admin.ModelAdmin):
    list_display = ('mother', 'pregnancy_order', 'year', 'mode_of_delivery', 'birth_weight', 'outcome')
    search_fields = ('mother__name', 'mode_of_delivery', 'outcome')

class ChildProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'mothers_profile')
    list_display_links = ('id', 'name')

class ImmunizationAdmin(admin.ModelAdmin):
    list_display = ('child', 'created_at', 'administered_by', 'get_vaccines_given')
    list_filter = ('created_at', 'administered_by')
    search_fields = ('child__name', 'batch_number', 'administered_by')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Child Information', {'fields': ('child',)}),
        ('BCG Vaccine', {
            'fields': (
                'bcg_date_given', 'bcg_next_visit', 
                'bcg_scar_checked', 'bcg_scar_present', 
                'bcg_repeated_date'
            ),
            'classes': ('collapse',)
        }),
        ('Polio Vaccines', {
            'fields': (
                ('opv_birth_date', 'opv_birth_next_date'),
                ('opv1_date', 'opv1_next_date'),
                ('opv2_date', 'opv2_next_date'),
                ('opv3_date', 'opv3_next_date'),
                ('ipv_date', 'ipv_next_date'),
            ),
            'classes': ('collapse',)
        }),
        ('Pentavalent Vaccines', {
            'fields': (
                ('penta1_date', 'penta1_next_date'),
                ('penta2_date', 'penta2_next_date'),
                ('penta3_date', 'penta3_next_date'),
            ),
            'classes': ('collapse',)
        }),
        ('PCV Vaccines', {
            'fields': (
                ('pcv1_date', 'pcv1_next_date'),
                ('pcv2_date', 'pcv2_next_date'),
                ('pcv3_date', 'pcv3_next_date'),
                'pcv_injection_site'
            ),
            'classes': ('collapse',)
        }),
        ('Rotavirus Vaccines', {
            'fields': (
                ('rota1_date', 'rota1_next_date'),
                ('rota2_date', 'rota2_next_date'),
                ('rota3_date', 'rota3_next_date'),
                'rota_administered_by',
                'rota_reaction'
            ),
            'classes': ('collapse',)
        }),
        ('MR Vaccines', {
            'fields': (
                ('mr6_date', 'mr6_next_date'),
                ('mr9_date', 'mr9_next_date'),
                ('mr18_date', 'mr18_next_date'),
            ),
            'classes': ('collapse',)
        }),
        ('Yellow Fever', {
            'fields': ('yf_date', 'yf_next_date', 'yf_eligible'),
            'classes': ('collapse',)
        }),
        ('Other Vaccines', {
            'fields': (
                ('other_vaccine1_name', 'other_vaccine1_date'),
                ('other_vaccine2_name', 'other_vaccine2_date'),
            ),
            'classes': ('collapse',)
        }),
        ('Adverse Events', {
            'fields': (
                'aefi_date', 'aefi_description', 'aefi_vaccine',
                'aefi_batch_number', 'aefi_manufacturer',
                'aefi_manufacture_date', 'aefi_expiry_date',
                'aefi_reported'
            ),
            'classes': ('collapse',)
        }),
        ('Vitamin A Supplementation', {
            'fields': (
                ('vita6_age_given', 'vita6_date_given', 'vita6_next_date'),
                ('vita12_age_given', 'vita12_date_given', 'vita12_next_date'),
                ('vita18_age_given', 'vita18_date_given', 'vita18_next_date'),
                ('vita24_age_given', 'vita24_date_given', 'vita24_next_date'),
                ('vita30_age_given', 'vita30_date_given', 'vita30_next_date'),
                ('vita36_age_given', 'vita36_date_given', 'vita36_next_date'),
            ),
            'classes': ('collapse',)
        }),
        ('Deworming', {
            'fields': (
                ('deworm12_age_given', 'deworm12_date_given', 'deworm12_next_date', 'deworm12_dosage'),
                ('deworm18_age_given', 'deworm18_date_given', 'deworm18_next_date', 'deworm18_dosage'),
                ('deworm24_age_given', 'deworm24_date_given', 'deworm24_next_date', 'deworm24_dosage'),
                ('deworm30_age_given', 'deworm30_date_given', 'deworm30_next_date', 'deworm30_dosage'),
            ),
            'classes': ('collapse',)
        }),
        ('Administration Details', {
            'fields': (
                'batch_number', 'administered_by', 'notes',
                'created_at', 'updated_at'
            )
        }),
    )
    
    def get_vaccines_given(self, obj):
        vaccines = []
        if obj.bcg_date_given: vaccines.append('BCG')
        if obj.opv1_date or obj.opv2_date or obj.opv3_date: vaccines.append('OPV')
        if obj.ipv_date: vaccines.append('IPV')
        if obj.penta1_date or obj.penta2_date or obj.penta3_date: vaccines.append('PENTA')
        if obj.pcv1_date or obj.pcv2_date or obj.pcv3_date: vaccines.append('PCV')
        if obj.rota1_date or obj.rota2_date or obj.rota3_date: vaccines.append('ROTA')
        if obj.mr6_date or obj.mr9_date or obj.mr18_date: vaccines.append('MR')
        if obj.yf_date: vaccines.append('YF')
        return ', '.join(vaccines) if vaccines else 'None'
    get_vaccines_given.short_description = 'Vaccines Given'

# Register all models
admin.site.register(HospitalUser, HospitalUserAdmin)


admin.site.register(MaternalProfile, MaternalProfileAdmin)
admin.site.register(PreviousPregnancy, PreviousPregnancyAdmin)
admin.site.register(ChildProfile, ChildProfileAdmin)
admin.site.register(Immunization, ImmunizationAdmin)