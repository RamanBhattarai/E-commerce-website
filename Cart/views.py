from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CartItem
from .forms import CartItemForm


# Create your views here.
@login_required(login_url='login')
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'cart_view.html', {'cart_items': cart_items})


@login_required(login_url='login')
def add_to_cart(request):
    if request.method == 'POST':
        form = CartItemForm(request.POST)
        if form.is_valid():
            cart_item = form.save(commit=False)
            cart_item.user = request.user
            cart_item.save()
            return render(request, 'cart_view.html', {'cart_items': [cart_item], 'total_price': cart_item.total_price})
    else:
        form = CartItemForm()
    return render(request, 'add_to_cart.html', {'form': form})


@login_required(login_url='login')
def clear_cart(request):
    CartItem.objects.filter(user=request.user).delete()
    return render(request, 'cart_view.html', {'cart_items': [], 'total_price': 0.00})
