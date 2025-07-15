from django.db import models

# Create your models here.
class OrderList(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField('Product', through='CartItem')
    quantity = models.DecimalField(max_digits=5, decimal_places=None, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    order_status = ['completed', 'pending', 'on-the-way']
    
    status = models.Choices(order_status, default='pending')
    
    def calculate_total(self):
        self.total_price = sum(item.product.price * item.quantity for item in self.cartitem_set.all())
        self.save()
    
    def __str__(self):
        return f"Delivery List of {self.user.username} created at {self.created_at}"