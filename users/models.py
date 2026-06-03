from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('client', 'Client'),
    )
    role = models.CharField(max_length=20,choices=ROLE_CHOICES,default="client")
    email  = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, unique=True)
    is_verified = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    def __str__(self):
        return f"{self.email}"

