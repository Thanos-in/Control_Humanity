from django.db import models
from django.conf import settings
from django.utils import timezone

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    director = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='directed_projects',
        limit_choices_to={'role': 'director'}
    )
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='managed_projects',
        null=True,
        blank=True,
        limit_choices_to={'role': 'manager'}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    data_input = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
