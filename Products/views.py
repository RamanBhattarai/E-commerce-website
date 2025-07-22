from .models import Category, Product
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm, ProductDescriptionFormSet
from django.db.models import Avg, Q, Count
from django.shortcuts import render


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        formset = ProductDescriptionFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            product = form.save()
            descriptions = formset.save(commit=False)
            for desc in descriptions:
                desc.product = product
                desc.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
        formset = ProductDescriptionFormSet()

    return render(request, 'Products/product_form.html', {'form': form, 'formset': formset})


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ProductDescriptionFormSet(request.POST, instance=product)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
        formset = ProductDescriptionFormSet(instance=product)
    return render(request, 'Products/product_form.html', {'form': form, 'formset': formset})


def product_list(request, pk=None, category_id=None):
    latest_products = Product.objects.order_by('-created_at')
    category_data = []

    for category in Category.objects.all():
        category_products = Product.objects.filter(category=category).order_by('-created_at')
        
        if category_products.count() >= 3 and category_products.first() in latest_products[:10]:
            category_data.append({
                'category': category,
                'products': category_products[:9]
            })

        if len(category_data) == 5:
            break
        
    top_sellers = get_top_sellers()
    
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category).order_by('-created_at')
    if pk:
        products = Product.objects.filter(category_id=pk).order_by('-created_at')
        category = Category.objects.get(pk=pk)
    else:
        products = Product.objects.all().order_by('-created_at')
        category = None

    context = {
        'category_data': category_data,
        'top_sellers': top_sellers,
        'products': products,
        'selected_category': category,
    }
    return render(request, 'Products/product_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product.objects.annotate(avg_rating=Avg('reviews__rating')),pk=pk)

    # Get related products (same category, exclude self)
    related_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:6]
    
    latest_products = Product.objects.order_by('-created_at')
    category_data = []

    for category in Category.objects.all():
        category_products = Product.objects.filter(category=category).order_by('-created_at')
        
        if category_products.count() >= 3 and category_products.first() in latest_products[:10]:
            category_data.append({
                'category': category,
                'products': category_products[:9]
            })

        if len(category_data) == 5:
            break

    context = {
        'product': product,
        'related_products': related_products,
        'category_data': category_data,
        'descriptions': product.descriptions.all(),  # get all key-value description entries
        'product_reviews': product.reviews.all()
    }
    return render(request, 'Products/product_detail.html', context)


def rated_products_by_range(request):
    latest_products = Product.objects.order_by('-created_at')
    category_data = []

    for category in Category.objects.all():
        category_products = Product.objects.filter(category=category).order_by('-created_at')
        
        if category_products.count() >= 3 and category_products.first() in latest_products[:10]:
            category_data.append({
                'category': category,
                'products': category_products[:9]
            })

        if len(category_data) == 5:
            break
        
    top_sellers = get_top_sellers()
    
    # Get min and max from query params (e.g., ?min=3&max=4)
    min_rating = request.GET.get('min')
    max_rating = request.GET.get('max')

    products = Product.objects.annotate(avg_rating=Avg('reviews__rating'))

    try:
        if min_rating is not None and max_rating is not None:
            min_val = float(min_rating)
            max_val = float(max_rating)
            products = products.filter(avg_rating__gte=min_val, avg_rating__lte=max_val)
    except ValueError:
        pass  # Ignore filtering if values are invalid

    products = products.order_by('-avg_rating')
    
    context = {
        'category_data': category_data,
        'top_sellers': top_sellers,
        'products': products,
        'min_rating': min_rating,
        'max_rating': max_rating,
    }

    return render(request, 'Products/product_list.html', context)


def product_search(request):
    latest_products = Product.objects.order_by('-created_at')
    category_data = []

    for category in Category.objects.all():
        category_products = Product.objects.filter(category=category).order_by('-created_at')
        
        if category_products.count() >= 3 and category_products.first() in latest_products[:10]:
            category_data.append({
                'category': category,
                'products': category_products[:9]
            })

        if len(category_data) == 5:
            break
        
    top_sellers = get_top_sellers()
    
    query = request.GET.get('q')
    products = Product.objects.none()

    if query:
        products = Product.objects.filter(Q(name__icontains=query)).distinct().order_by('-created_at')
        
    if not products:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(descriptions__value__icontains=query)
        ).distinct().order_by('-created_at')
    
    context = {
        'category_data': category_data,
        'top_sellers': top_sellers,
        'products': products,
        'query': query
    }

    return render(request, 'Products/product_list.html', context)


def get_top_sellers(limit=5):
    top_products = Product.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        num_reviews=Count('reviews')
    ).filter(avg_rating__isnull=False).order_by('-avg_rating', '-num_reviews')[:limit]
    return top_products
