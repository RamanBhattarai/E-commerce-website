from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    full_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    preferred_shipping_address = models.TextField(blank=True)

    def __str__(self):
        return self.username
