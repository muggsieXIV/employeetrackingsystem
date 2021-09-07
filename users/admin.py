from django.contrib import admin
from .models import Admin


# Register your models here.
@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ['id', 'last_name', 'first_name', 'email', 'password', 'company', 'created_at', 'updated_at']
