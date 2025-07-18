from django.db import models
from django.conf import settings
from Orders.models import Order


# Create your models here.
class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        UNPAID = "unpaid", "Unpaid"
        PAID = "paid", "Paid"
        
    class PaymentMethod(models.TextChoices):
        DIGITAL = "digital", "Digital"
        CASH_ON_DELIVERY = "cash_on_delivery", "Cash On Delivery"
      
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length= 20,
        choices= PaymentStatus.choices,
        default= PaymentStatus.UNPAID
        )
    method = models.CharField(
        max_length=20,
        choices= PaymentMethod.choices,
        default= PaymentMethod.DIGITAL
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment {self.payment_id} - {self.status}"
    
    class Meta:
        ordering = ['-created_at']
