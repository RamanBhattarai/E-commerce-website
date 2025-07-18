from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from Orders.models import Order
from .models import Payment
import requests, os


KHALTI_SECRET_KEY = os.getenv('KHALTI_SECRET_KEY')

def checkout(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    context = {
        'order': order,
        'amount_paisa': int(order.total_price * 100),
        'khalti_public_key': os.getenv('KHALTI_PUBLIC_KEY'),
        'csrf_token': request.COOKIES.get('csrftoken')
    }
    return render(request, 'Payments/checkout.html', context)

@csrf_exempt
def khalti_verify(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        amount = int(request.POST.get('amount'))
        order_number = request.POST.get('order_number')

        if not all([token, amount, order_number]):
            return HttpResponseBadRequest("Missing fields")

        order = get_object_or_404(Order, order_number=order_number, user=request.user)

        response = requests.post(
            url="https://khalti.com/api/v2/payment/verify/",
            data={
                'token': token,
                'amount': amount
            },
            headers={
                'Authorization': f'Key {KHALTI_SECRET_KEY}'
            }
        )

        resp_data = response.json()

        if response.status_code == 200 and 'idx' in resp_data:
            # Save Payment record
            Payment.objects.create(
                user=request.user,
                order=order,
                payment_id=resp_data['idx'],
                amount=amount / 100,  # Convert paisa to rupees
                status=Payment.PaymentStatus.PAID,
                method=Payment.PaymentMethod.DIGITAL,
            )

            return JsonResponse({'success': True, 'message': 'Payment verified'})
        else:
            return JsonResponse({'success': False, 'error': resp_data.get('detail', 'Verification failed')})


def payment_success(request):
    return render(request, 'Payments/success.html')