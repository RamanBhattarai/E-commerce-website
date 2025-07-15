from django.shortcuts import render
from .models import DeliveryList
from .forms import DeliveryListForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def delivery(request):
    delivery_object = DeliveryList.objects.filter(user=request.user)
    return render(request, 'orders.html', {'delivery_object':delivery_object})


@login_required(login_url='login')
def cancel_delivery(request):
    DeliveryList.objects.filter(user=request.user).delete()
    return render(request, 'cart_view.html', {'cart_items': [], 'total_price': 0.00})
