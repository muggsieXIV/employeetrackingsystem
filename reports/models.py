from django.db import models
import re  # in order to use the regex module
from datetime import date, datetime, timedelta  # to use the current date
from users.models import Admin
from employees.models import Employee
from company.models import Company, Location


class ClockSystemManager(models.Manager):
    def clockSystem_validator(self, form_data):
        errors = {}
        if len(form_data['employee']) <= 0:
            errors['employee'] = "No employee was selected, try again"
        return errors
    def clockin_validator(self, form_data):
        errors = {}
        if len(form_data['comment']) == 1:
            errors['comment'] = "Please be descriptive if there is an issue."
        return errors
    def clockout_validator(self, form_data):
        errors = {}
        if len(form_data['comment']) == 1:
            errors['comment'] = "Please be descriptive if there is an issue."
        return errors

class ClockSystem(models.Model):
    employee=models.ForeignKey(Employee, related_name="clockin_employee", on_delete=models.CASCADE)
    location=models.ForeignKey(Location, related_name="clockin_location", on_delete=models.CASCADE)
    role=models.CharField(max_length=80, null=True, default="None")
    time_worked=models.CharField(max_length=255, null=True, default="00:00:00")
    in_comment=models.TextField(null=True, default="None")
    out_comment=models.TextField(null=True, default="None")
    date_in=models.DateField(null=True)
    date_out=models.DateField(null=True)
    clocked_in_at=models.TimeField(null=False)
    clocked_out_at=models.TimeField(null=True)
    is_flagged=models.BooleanField(default=False)
    objects=ClockSystemManager()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        ordering = (
            'id',
            'is_flagged',
            'employee',
            'date_in',
            'date_out',
            'clocked_in_at',
            'clocked_out_at',
            'time_worked',
            'role',
            'location',
            'in_comment',
            'out_comment',
            'created_at',
            'updated_at'
        )


