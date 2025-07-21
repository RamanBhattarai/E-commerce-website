from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client
import os, random
from .models import PhoneOTP
from django.http import JsonResponse


def send_otp_to_phone(phone_number):
    otp_code = str(random.randint(100000, 999999))  # 6-digit OTP

    # Save to DB (update if exists)
    PhoneOTP.objects.update_or_create(
        phone_number=phone_number,
        defaults={'otp': otp_code}
    )

    # Send SMS via Twilio
    client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

    message = client.messages.create(
        body=f"Your verification code is: {otp_code}",
        from_='+1234567890',  # Twilio number
        to=str(phone_number)
    )
    return True


def send_otp(request):
    phone = request.POST.get('phone')
    if phone:
        send_otp_to_phone(phone)
        return JsonResponse({'success': True, 'message': 'OTP sent successfully'})
    return JsonResponse({'success': False, 'message': 'Phone number is required'})



def send_order_email(user, order, invoice_url):
    subject = 'Order Confirmation'
    message = (
        f'Thank you {user.full_name}, your order #{order.order_number} is confirmed.\n\n'
        f'You can download the invoice here: {invoice_url}\n\n'
        f'Details:\n{order}'
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

def send_order_sms(to_phone, order, invoice_url):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Hi! Your order #{order.order_number} is confirmed. Invoice: {invoice_url}",
        from_='+1234567890',  # your Twilio number
        to=to_phone
    )
