
from django.db import models
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count
# from users import models

class AttendanceRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    scanned_at = models.DateTimeField(auto_now_add=True)  # Check-in time
    checked_out_at = models.DateTimeField(null=True, blank=True)  # Check-out time
    date =models.DateField(default=timezone.now())
    status =models.CharField(max_length=20, choices=[('scanned_at','scanned_at'),('check_out_at','check_out_at')])
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    STATUS_CHOICES = [
    ('Present', 'Present'),
    ('Late', 'Late'),
    ('Absent', 'Absent'),
]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    

    def duration(self):
        if self.scanned_at and self.checked_out_at:
            return self.checked_out_at - self.scanned_at
        return timedelta(0)

    def is_present(self):
        return self.duration().total_seconds() >= 1800  # Minimum 30 minutes present

    def __str__(self):
        return f"{self.user.username} - {self.date}"


    # def __str__(self):
    #     return f"{self.user.username} @ {self.scanned_at.strftime('%Y-%m-%d %H:%M')}"
    


    @property
    def hours_worked(self):
        if self.checked_out_at:
            # get time difference
            delta = self.checked_out_at - self.scanned_at
            total_seconds = int(delta.total_seconds())

            # calculate hours, minutes, seconds
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600 ) // 60
            seconds = total_seconds % 60
            return f"{hours} H - {minutes} M - {seconds} S"
        return "----"
    

class PasswordResetLog(models.Model):

    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    email_entered = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.email_entered} | {self.status} | {self.timestamp}"












