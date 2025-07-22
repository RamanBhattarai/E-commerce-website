from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Products.models import Product
from .models import Review

@login_required(login_url='login')
def submit_review(request, pk):
    product = get_object_or_404(Product, id=pk)

    if request.method == 'POST':
        review_text = request.POST.get('review')
        rating = request.POST.get('rating')

        if review_text and rating:
            # Check for existing review
            review, created = Review.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={
                    'review': review_text,
                    'rating': int(rating)
                }
            )

            if not created:
                # If already exists, update it
                review.review = review_text
                review.rating = int(rating)
                review.save()
                messages.success(request, 'Your review has been updated.')
            else:
                messages.success(request, 'Your review has been submitted.')
        else:
            messages.error(request, 'Please provide both a review and a rating.')

    return redirect('product_detail', pk=product.id)
