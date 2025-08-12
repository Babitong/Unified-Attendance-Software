
from django.db import models
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count

class AttendanceRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    scanned_at = models.DateTimeField(auto_now_add=True)  # Check-in time
    checked_out_at = models.DateTimeField(null=True, blank=True)  # Check-out time
    date =models.DateField(default=timezone.now())
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    

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









# from django.db import models
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class Classroom(models.Model):
#     name = models.CharField(max_length=100)
#     qr_code = models.ImageField(upload_to='qrcodes/', blank=True)
#     latitude = models.DecimalField(max_digits=9, decimal_places=6)
#     longitude = models.DecimalField(max_digits=9, decimal_places=6)

#     def save(self, *args, **kwargs):
#         if not self.qr_code:  # Generate QR on first save
#             self.generate_qr_code()
#         super().save(*args, **kwargs)

#     def generate_qr_code(self):
#         # Implementation from previous QR generation code
#         pass

# class AttendanceLog(models.Model):
#     LOG_TYPES = [
#         ('CHECK_IN', 'General Check-in'),
#         ('CHECK_OUT', 'General Check-out'),
#         ('CLASS_START', 'Class Start'),
#         ('CLASS_END', 'Class End'),
#     ]
    
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     log_type = models.CharField(max_length=20, choices=LOG_TYPES)
#     classroom = models.ForeignKey(Classroom, null=True, blank=True, on_delete=models.SET_NULL)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     latitude = models.FloatField(null=True, blank=True)
#     longitude = models.FloatField(null=True, blank=True)
#     is_offline = models.BooleanField(default=False)



