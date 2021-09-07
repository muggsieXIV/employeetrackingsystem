from django.contrib import admin
from .models import Company, Location


# Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image', 'created_at', 'updated_at']

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address', 'city', 'state', 'username', 'password', 'company', 'created_at', 'updated_at']

