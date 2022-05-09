from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):   
    dateOfBirth = models.DateField(null=True)
    gender = models.CharField(max_length=6, null=True)
    phone = models.CharField(max_length=15, null=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=100, null=True)
    is_email_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username