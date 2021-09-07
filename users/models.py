from django.db import models
import re  # in order to use the regex module
from company.models import Company


class AdminManager(models.Manager):
    # create validations - one for registration, one for login
    def admin_validator(self, post_data):
        errors = {}

        # regex imported above
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        # test whether a field matches the pattern
        # The EMAIL_REGEX object has a method called .match() that will return None if no match can be found. If the argument matches the regular expression, a match object instance is returned.
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email address!"

        # First Name - required; at least 2 characters; letters only
        if len(post_data['first_name']) == 0:
            errors['first_name'] = "First name required"

        if len(post_data['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters"

        # returns a boolean that shows whether a string contains only alphabetic characters
        if not str.isalpha(post_data['first_name']):
            errors['first_name'] = "First name must be letters only"

        # Last Name - required; at least 2 characters; letters only
        if len(post_data['last_name']) == 0:
            errors['last_name'] = "Last name required"

        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters"

        # returns a boolean that shows whether a string contains only alphabetic characters
        if not str.isalpha(post_data['last_name']):
            errors['last_name'] = "Last name must be letters only"

            # Password - required; at least 8 characters; matches password confirmation
        if len(post_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"

        if post_data['password'] != post_data['password_confirm']:
            errors['password_confirm'] = "Passwords must match"
            
        return errors

    def login_validator(self, post_data):
        errors = {}

        # regex imported above
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        # test whether a field matches the pattern
        # The EMAIL_REGEX object has a method called .match() that will return None if no match can be found. If the argument matches the regular expression, a match object instance is returned.
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email address or password!"

        # Password - required; at least 8 characters; matches password confirmation
        if (len(post_data['password']) < 8):
            errors['password'] = "Invalid email address or password!"

        return errors

    def delete_validator(self, post_data):
        errors = {}
        return errors


class Admin(models.Model):
    # user information
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    company = models.ForeignKey(Company, related_name="admins", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # add for manager validator
    objects = AdminManager()

    class Meta:
        ordering = (
            'id',
            'last_name',
            'first_name',
            'email',
            'password',
            'company',
            'created_at',
            'updated_at'
        )

    def __str__(self):
        return(self.last_name + ', ' + self.first_name)
