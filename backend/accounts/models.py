from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('employee', 'Employee'),
        ('manager', 'Manager'),
        ('director', 'Director'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def is_employee(self):
        return self.role == 'employee'

    def is_manager(self):
        return self.role == 'manager'

    def is_director(self):
        return self.role == 'director'
