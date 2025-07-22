from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Order
from Cart.models import Cart, CartItem
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from Payments.models import Payment



@login_required(login_url='login')
def order_view(request):
    orders = Order.objects.filter(user=request.user).exclude(status='cancelled').order_by('-created_at')

    order_list = []
    for order in orders:
        order_list.append({
            'order_number': order.order_number,
            'status': order.status,
            'created_at': order.created_at,
            'total_price': order.total_price,
        })

    return render(request, 'Orders/order_view.html', {'orders': order_list})


@login_required(login_url='login')
def order_details_view(request, order_number):
    
    order = get_object_or_404(Order, user=request.user, order_number=order_number)
    order_items = order.items.all()
    total_price = order.total_price
    payment = Payment.objects.filter(order=order).first()

    return render(request, 'Orders/order_details_view.html', {
        'order': order,
        'order_items': order_items,
        'total_price': total_price,
        'payment': payment,
    })


@login_required(login_url='login')
def place_order(request):
    # Make sure the cart exists and is not empty
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart or not cart_items.exists():
        return redirect('cart_view')

    # Temporarily store a flag or cart_id in session
    request.session['placing_order'] = True
    return redirect('delivery')


@login_required(login_url='login')
def order_history(request):
    # Fetch all completed orders for the logged-in user
    orders = Order.objects.filter(user=request.user, status='completed')
    order_list = []
    for order in orders:
        order_list.append({
            'order_number': order.order_number,
            'status': order.status,
            'created_at': order.created_at,
            'total_price': order.total_price(),
        })

    return render(request, 'Orders/order_history.html', {'orders': order_list})


@login_required(login_url='login')
def cancel_order(request, order_number):
    order = get_object_or_404(Order, user=request.user, order_number=order_number)
    order.status = 'cancelled' 
    order.save()
    return redirect('order_view')



@login_required(login_url='login')
def invoice_generation(request, order_number):
    order = get_object_or_404(Order, user=request.user, order_number=order_number)

    # Create PDF buffer
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    # Set basic layout
    y = 800
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, f"Invoice - Order #{order.order_number}")
    y -= 30

    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"Customer: {order.user.username}")
    y -= 20
    p.drawString(50, y, f"Date: {order.created_at.strftime('%Y-%m-%d %H:%M')}")
    y -= 40

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Product")
    p.drawString(300, y, "Quantity")
    p.drawString(400, y, "Price")
    y -= 20

    total_price = 0
    p.setFont("Helvetica", 12)

    for item in order.items.all():
        p.drawString(50, y, item.product.name)
        p.drawString(300, y, str(item.quantity))
        item_total = item.product.price * item.quantity
        p.drawString(400, y, f"${item_total:.2f}")
        total_price += item_total
        y -= 20
        if y < 100:  # Avoid writing too low on the page
            p.showPage()
            y = 800
            p.setFont("Helvetica", 12)

    y -= 20
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, f"Total: ${total_price:.2f}")

    p.showPage()
    p.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf', headers={
        'Content-Disposition': f'attachment; filename="Invoice_Order_{order.order_number}.pdf"'
    })    