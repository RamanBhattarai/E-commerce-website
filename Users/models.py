from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    full_name = models.CharField(max_length=255, blank=True)
    phone_number = PhoneNumberField(blank=False, null=False, region='NP')
    is_phone_verified = models.BooleanField(default=False)
    address = models.TextField(blank=True)
    preferred_shipping_address = models.TextField(blank=True)

    def __str__(self):
        return self.username
