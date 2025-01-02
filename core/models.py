from django.conf import settings
from django.db import models


class Task(models.Model):
    PRIORITY_CHOICES = {
        'H': 'High',
        'N': 'Normal',
        'L': 'Low'
    }

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    description = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='L')
    added_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)