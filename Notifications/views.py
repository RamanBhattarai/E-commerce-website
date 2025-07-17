from django.http import JsonResponse
from .models import PhoneOTP
from Users.models import UserProfile

def verify_otp(request):
    phone = request.POST.get('phone')
    otp = request.POST.get('otp')

    try:
        record = PhoneOTP.objects.get(phone_number=phone)
        if record.otp == otp and not record.is_expired():
            user = UserProfile.objects.get(phone_number=phone)
            user.is_phone_verified = True
            user.save()
            record.delete()  # remove used OTP
            return JsonResponse({'success': True, 'message': 'Phone verified successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid or expired OTP.'})
    except PhoneOTP.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Phone not found.'})

