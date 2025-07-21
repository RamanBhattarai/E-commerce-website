from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Products.models import Product
from .models import Review

@login_required(login_url='login')
def submit_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        review_text = request.POST.get('review')
        rating = request.POST.get('rating')

        if review_text and rating:
            Review.objects.create(
                user=request.user,
                product=product,
                review=review_text,
                rating=int(rating)
            )
            messages.success(request, 'Your review has been submitted.')
        else:
            messages.error(request, 'Please provide both a review and a rating.')

    return redirect('product_detail', product_id=product.id)
