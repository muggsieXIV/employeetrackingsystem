from django.contrib import admin
from .models import Company, Location, CompanySetting


# Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image', 'created_at', 'updated_at']

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address', 'city', 'state', 'username', 'password', 'company', 'created_at', 'updated_at']

@admin.register(CompanySetting)
class CompanySettingAdmin(admin.ModelAdmin):
    list_display = ['id', 'company', 'color', 'font_color', 'background_color', 'time_zone', 'contact_name', 'contact_number', 'created_at', 'updated_at']
