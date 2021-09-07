from django.db import models
from company.models import Company


# Create your models here.
class EmployeeManager(models.Manager):
    def employee_validator(self, form_data):
        errors = {}
        if len(form_data['first_name']) < 2:
            errors['first_name'] = "First Name is not long enough. Try again!"
        if len(form_data['last_name']) < 2:
            errors['last_name'] = "Last Name is not long enough. Try again!"
        if len(form_data['role']) < 2:
            errors['role'] = "Role must be at least two characters. Try again!"
        return errors

class Employee(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    is_active=models.BooleanField(default=False)
    role=models.CharField(max_length=255, default="Not Provide")
    objects=EmployeeManager()
    company=models.ForeignKey(Company, related_name="employee", on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        ordering = (
            'id',
            'last_name',
            'first_name',
            'is_active',
            'role',
            'company'
        )

    def __str__(self):
        return(self.last_name + ', ' + self.first_name)
