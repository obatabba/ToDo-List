from datetime import datetime, time, timedelta
from django.utils.timezone import now, get_current_timezone, localtime, localdate
from django.conf import settings
from django.db import models


def default_deadline():
    return datetime.combine(now().date() + timedelta(days=1), time(), tzinfo=get_current_timezone())


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
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.deadline is None:
            self.deadline = default_deadline()
        super().save(*args, **kwargs)


    @property
    def is_overdue(self):
        """Determine if the task is overdue based on user's time zone."""
        if not self.is_completed:
            # Convert deadline to user's time zone
            user_deadline = localtime(value=self.deadline)
            # Get the current time in user's time zone
            user_current_time = localtime()
            return user_deadline < user_current_time
        return False

    def __str__(self):
        # deadline = localtime(self.deadline)
        deadline = localtime(value=self.deadline)
        if deadline == default_deadline():
            return f"{self.title} | deadline: End of today"
        elif deadline.date() == localdate() + timedelta(days=1): 
            return f"{self.title} | deadline: Tomorrow {deadline:%I:%M %p}"
        return f"{self.title} | deadline: {deadline:%a %d %b %I:%M %p}"
