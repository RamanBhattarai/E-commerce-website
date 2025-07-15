from django.db import models

# Create your models here.
class DeliveryList(models.Model):
    address = models.ForeignKey('auth.User.address', on_delete=models.CASCADE)
    
    
    delivery_method = ['Standard', 'Express', 'Next Day']
    delivery_status = models.Choices(delivery_method)
    
    