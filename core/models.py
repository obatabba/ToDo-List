from django.utils.timezone import now, localtime
from django.conf import settings
from django.db import models
import pytz


def default_deadline():
    return now().replace(hour=23, minute=59, second=59)


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
    deadline = models.DateTimeField(default=default_deadline)
    is_completed = models.BooleanField(default=False)

    @property
    def is_overdue(self):
        """Determine if the task is overdue based on user's time zone."""
        if self.is_completed:
            return True
        else:
            user_tz = pytz.timezone('Asia/Damascus') # test timezone

            # Convert deadline to user's time zone
            user_deadline = self.deadline.astimezone(user_tz)
            user_current_time = localtime(timezone=user_tz)
            return user_deadline < user_current_time
        
    # def __str__(self):
    #     return f'{self.title} | {self.priority} | deadline: {self.deadline}'
