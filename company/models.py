from django.db import models
import re  # in order to use the regex module


class CompanyManager(models.Manager):
    def company_validator(self, form_data):
        errors = {}
        if len(form_data['name']) < 2:
            errors['name'] = "Name must be at least two characters."
        return errors


class Company(models.Model):
    name=models.CharField(max_length=100, null=False, unique=True)
    image=models.ImageField(null=True, upload_to="company/")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects = CompanyManager()
    # add for manager validator

    class Meta:
        ordering = (
            'id',
            'name',
            'image',
            'created_at',
            'updated_at'
        )

    def __str__(self):
        return self.name


class LocationManager(models.Manager):
    def location_validator(self, form_data):
        errors = {}
        if len(form_data['name']) < 2:
            errors['name'] = "Name must be descriptive."
        if len(form_data['address']) < 5:
            errors['address'] = "Please use your full street address."
        if len(form_data['state']) < 4:
            errors['state'] = "Please use the full state name."
        if len(form_data['username']) < 4:
            errors['username'] = "Username must be at least 4 characters."
        if len(form_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        return errors
    def login_validator(self, form_data):
        errors = {}
        if not len(form_data['username']):
            errors['username'] = "Username doesn't match out records. Try again."
        return errors

class Location(models.Model):
    address=models.CharField(max_length=200, null=False)
    city=models.CharField(max_length=200, null=False)
    state=models.CharField(max_length=200, null=False)
    country=models.CharField(max_length=200, null=True)
    name=models.CharField(max_length=200, null=False)
    username=models.CharField(max_length=30, null=False)
    password=models.CharField(max_length=30, null=False)
    company=models.ForeignKey(Company, related_name="location", on_delete=models.CASCADE)
    objects=LocationManager()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        ordering = (
            'id',
            'company',
            'name', 
            'address',
            'city',
            'state',
            'username',
            'password',
            'created_at',
            'updated_at' 
        )

    def __str__(self):
        return self.name

class CompanySetting(models.Model):
    company=models.ForeignKey(Company, related_name="company_settings", on_delete=models.CASCADE)
    color=models.CharField(max_length=100, null=True, default="#26225B")
    font_color=models.CharField(max_length=100, null=True, default="#F8F8F8")
    background_color=models.CharField(max_length=50, null=True, default="#F8F8F8")
    time_zone=models.CharField(max_length=200, null=True, default="US/Central")
    contact_name=models.CharField(max_length=50, null=True)
    contact_number=models.CharField(max_length=14, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company.name

    class Meta:
        ordering = (
            'id',
            'company',
            'color',
            'font_color',
            'background_color',
            'time_zone',
            'contact_name',
            'contact_number',
            'created_at',
            'updated_at'
        )
