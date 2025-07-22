from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from Orders.models import Order
from .models import Payment
import requests, os
from django.contrib.auth.decorators import login_required
import uuid


KHALTI_SECRET_KEY = os.getenv('KHALTI_SECRET_KEY')

@login_required(login_url='login')
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

@login_required(login_url='login')
def payment_success(request):
    order = Order.objects.filter(user=request.user).order_by('-created_at').first()
    return render(request, 'Payments/success.html', {'order': order})

@login_required(login_url='login')
def payment_method(request, order_number):
    if request.method == "POST":
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
        method = request.POST.get('method')
        total_price = order.total_price or 0
        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={
                'user': request.user,
                'amount': total_price,
                'status': Payment.PaymentStatus.UNPAID,
                'method': method,
                'payment_id': str(uuid.uuid4()),
            }
        )
        if not created:
            payment.method = method
            payment.amount = total_price
            payment.save()
        return redirect('order_details_view', order_number=order.order_number)

    return redirect('order_view')
