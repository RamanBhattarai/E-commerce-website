from django.db import models
from Products.models import Product
from Delivery.models import DeliveryList
import uuid
from django.conf import settings

# Create your models here.  
class Order(models.Model):
    class OrderStatus(models.TextChoices):
        COMPLETED = "completed", "Completed"
        PENDING = "pending", "Pending"
        ON_THE_WAY = "on_the_way", "On The Way"
        CANCELLED = "cancelled", "Cancelled"
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    delivery_method = models.ForeignKey(DeliveryList, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )    

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"Orders of {self.user.username} created at {self.created_at}"
       
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in order {self.order.id}"