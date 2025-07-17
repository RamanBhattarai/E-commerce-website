import random
from django.db import models
from django.utils import timezone
from datetime import timedelta
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class PhoneOTP(models.Model):
    phone_number = PhoneNumberField(unique=True, region='NP')
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)
