from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import CartItem, Cart, Wishlist, WishlistItem
from Products.models import Product
from django.http import JsonResponse


@login_required(login_url='login')
def cart_view(request):
    cart = Cart.objects.filter(user=request.user).first()
    
    if cart:
        cart_items = cart.items.all()
        total_price = cart.total_price()
    else:
        cart_items = []
        total_price = 0

    return render(request, 'Cart/cart_view.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
    cart_item.save()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': 'Product added to cart'})

    return redirect(request.META.get('HTTP_REFERER', 'homepage'))

@login_required(login_url='login')
def remove_from_cart(request, item_id):
    cart = Cart.objects.filter(user=request.user).first()

    if request.method == "POST" and cart:
        cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)
        cart_item.delete()

    return redirect('cart_view')


@login_required(login_url='login')
def clear_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    
    if cart:
        cart.items.all().delete()

    return redirect('cart_view')


@login_required(login_url='login')
def add_quantity(request, item_id):
    cart = Cart.objects.filter(user=request.user).first()

    if request.method == "POST" and cart:
        cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_view')

@login_required(login_url='login')
def subtract_quantity(request, item_id):
    cart = Cart.objects.filter(user=request.user).first()

    if request.method == "POST" and cart:
        cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)
        cart_item.quantity -= 1
        cart_item.save()

    return redirect('cart_view')


@login_required(login_url='login')
def wishlist(request):
    lists = Wishlist.objects.filter(user=request.user).first()
    
    if lists:
        wishlist_items = lists.items.all()
        total_price = lists.total_price()
    else:
        wishlist_items = []
        total_price = 0

    return render(request, 'Cart/wishlist.html', {'wishlist_items': wishlist_items, 'total_price': total_price})

from django.http import JsonResponse

@login_required(login_url='login')
def add_to_wishlist(request, item_id):
    product = get_object_or_404(Product, id=item_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    WishlistItem.objects.get_or_create(lists=wishlist, product=product)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': 'Product added to wishlist'})

    return redirect(request.META.get('HTTP_REFERER', 'homepage'))


@login_required(login_url='login')
def remove_from_wishlist(request, item_id):
    lists = Wishlist.objects.filter(user=request.user).first()

    if request.method == "POST" and lists:
        lists_item = get_object_or_404(WishlistItem, lists=lists, id=item_id)
        lists_item.delete()

    return redirect('wishlist')