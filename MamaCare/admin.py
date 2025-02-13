

# Register your models here.
from django.contrib import admin
from .models import MaternalProfile, HealthFacility

admin.site.register(MaternalProfile)


@admin.register(HealthFacility)
class HealthFacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')  # Show columns in admin panel
    search_fields = ('name', 'code')  # Enable search