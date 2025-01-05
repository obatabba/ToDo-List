from django.utils.timezone import now
from django.conf import settings
from django.db import models


class Task(models.Model):
    # PRIORITY_CHOICES is referenced in forms.py, 'rename' if necessary
    PRIORITY_CHOICES = {
        'L': 'Low',
        'N': 'Normal',
        'H': 'High'
    }

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    description = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='L')
    added_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    is_overdue = models.BooleanField(default=False)

    def check_overdue(self):
        """
        Set 'is_overdue' attribute to True for Task objects with deadline less than django.utils.timezone.now()
        """
        if self.deadline:
            if not self.is_overdue and self.deadline < now():
                self.is_overdue = True
                self.save()
