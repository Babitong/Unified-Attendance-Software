from django.db import models
from django.contrib.auth.models import AbstractUser
# from users.models import Department

USER_TYPE_CHOICES = (
        ('admin','Administrator'),
        ('teacher','Teacher'),
        ('secretary','Secretary'),
    )

# department class
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) :
        return self.name
    
class Timetable(models.Model):
    title = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    upload = models.FileField(upload_to='timetables/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    # def save(self, *args,**kwargs):
    #     super().save(*args, **kwargs)
    
# custom user class
class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=100, choices=USER_TYPE_CHOICES, null=True,blank=True)
    phone_number = models.CharField(max_length=20, null=True,blank=True)
    department = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self) :
        return f'{self.username} ({self.department})'

# Create your models here.
