from django.db.models.signals import post_save
from django.dispatch import receiver
from Orders.models import Order
from django.urls import reverse
from .services import send_order_email, send_order_sms

@receiver(post_save, sender=Order)
def send_order_notification(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        order_number = instance.order_number
        invoice_url = f"http://yourdomain.com{reverse('invoice_generation', args=[order_number])}"


        send_order_email(user, instance, invoice_url)
        send_order_sms(user.phone_number, instance, invoice_url)
