from .models import DeliveryList
from .forms import DeliveryListForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from Orders.models import Order, OrderItem
from Cart.models import Cart, CartItem


@login_required(login_url='login')
def delivery(request):
    if request.method == 'POST':
        form = DeliveryListForm(request.POST)
        if form.is_valid():
            delivery = form.save(commit=False)
            delivery.user = request.user
            delivery.save()

            #  Now create the order
            cart = Cart.objects.filter(user=request.user).first()
            cart_items = CartItem.objects.filter(cart=cart)

            if not cart or not cart_items.exists():
                return redirect('cart_view')

            order = Order.objects.create(
                user=request.user,
                delivery_method=delivery  # Assign the required delivery_method here
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                )

            cart_items.delete()
            return redirect('order_view')  # or wherever you want after placing the order

    else:
        form = DeliveryListForm()

    delivery_object = DeliveryList.objects.filter(user=request.user)
    return render(request, 'Delivery/delivery_method.html', {
        'form': form,
        'delivery_object': delivery_object
    })

