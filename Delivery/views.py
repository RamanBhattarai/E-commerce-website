from django.shortcuts import render, redirect
from .models import DeliveryList
from .forms import DeliveryListForm
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def delivery(request):
    if request.method == 'POST':
        form = DeliveryListForm(request.POST)
        if form.is_valid():
            delivery = form.save(commit=False)
            delivery.user = request.user
            delivery.save()
            return redirect('order_view')  # Redirect to the same page or a success page
    else:
        form = DeliveryListForm()
    delivery_object = DeliveryList.objects.filter(user=request.user)
    return render(request, 'Delivery/delivery_method.html', {
        'form': form,
        'delivery_object': delivery_object
    })