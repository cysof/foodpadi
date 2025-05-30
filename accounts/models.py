from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from decimal import Decimal
from django.conf import settings
from django.core.exceptions import ValidationError

class FarmPadiUser(AbstractUser):
    ACCOUNT_TYPE_CHOICES = (
        ('FARMER', 'Farmer'),
        ('BUYER', 'Buyer'),
        ('TRANSPORTER', 'Transporter'),
    )
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES)
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    other_name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=(
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    ))
    phone_number = models.CharField(max_length=12, null=True, blank=True, unique=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'username']
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.profile_type = self.account_type
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Profile(models.Model):
    PROFILE_TYPE_CHOICES = (
        ('FARMER', 'Farmer'),
        ('BUYER', 'Buyer'),
        ('TRANSPORTER', 'Transporter'),
    )
    user = models.OneToOneField(FarmPadiUser, on_delete=models.CASCADE,related_name='profile')
    profile_type = models.CharField(max_length=20, choices=PROFILE_TYPE_CHOICES)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f'Profile: {self.user.username}'
    
    