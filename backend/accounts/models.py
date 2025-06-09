from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('employee', 'Employee'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
        ('director', 'Director'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def is_employee(self):
        return self.role == 'employee'

    def is_manager(self):
        return self.role == 'manager'

    def is_director(self):
        return self.role == 'director'
