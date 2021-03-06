from django.contrib import admin
from .models import ClockSystem

# Register your models here.
@admin.register(ClockSystem)
class ClockSystemAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_flagged', 'flag_message', 'employee', 'date_in', 'date_out', 'clocked_in_at', 'clocked_out_at', 'time_worked', 'in_comment', 'out_comment', 'location_in', 'location_out', 'role', 'created_at', 'updated_at']
