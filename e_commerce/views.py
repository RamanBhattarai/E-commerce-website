# home/views.py
from django.shortcuts import render
from Products.models import Product, Category  # import from the correct app
from django.utils.timezone import now

def home(request):
    latest_products = Product.objects.order_by('-created_at')  # requires created_at field
    valid_categories = []

    for category in Category.objects.all():
        category_products = Product.objects.filter(category=category).order_by('-created_at')
        
        # Check: at least 3 products AND latest product belongs to this category
        if category_products.count() >= 3 and category_products.first() in latest_products[:10]:
            valid_categories.append({
                'category': category,
                'products': category_products[:9]
            })

        if len(valid_categories) == 5:
            break

    context = {
        'category_data': valid_categories,
        # ... any other data for homepage
    }

    return render(request, 'homepage.html', context)
