from django.db import models
from django.conf import settings


# Create your models here.
class DeliveryList(models.Model):
    class DeliveryMethod(models.TextChoices):
        STANDARD = "standard", "Standard"
        EXPRESS = "express", "Express"
        NEXT_DAY = "next_day", "Next Day"
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=100)
    delivery_method = models.CharField(
        max_length=20,
        choices=DeliveryMethod.choices,
        default=DeliveryMethod.STANDARD
    )
    
    
    def __str__(self):
        return f"Delivery for {self.user} via {self.delivery_method}"