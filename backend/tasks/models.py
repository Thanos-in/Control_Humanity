from django.db import models
from django.conf import settings
from projects.models import Project
from django.utils import timezone

class Status(models.Model):
    name = models.CharField(max_length=50)
    project = models.ForeignKey(
    Project,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    related_name='statuses'
    )
    order = models.PositiveIntegerField(default=0)
    color = models.CharField(max_length=7, default='#FFFFFF')

    class Meta:
        unique_together = ('name', 'project')
        ordering = ['order']

    def __str__(self):

            if self.project:
                return f"{self.project.name} – {self.name}"

            return self.name
    
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='tasks',
        null=True,
        blank=True,
        limit_choices_to={'role': 'employee'}
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='tasks'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tasks'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    data_input = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(null=True, blank=True)
    color = models.CharField(max_length=7, default='#FFFFFF')

    def __str__(self):
        return f"{self.title} ({self.project.name})"
