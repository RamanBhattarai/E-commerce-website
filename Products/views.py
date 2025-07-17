from .models import Category, Product
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm, ProductDescriptionFormSet
from django.db.models import Avg
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

    return render(request, 'product_form.html', {'form': form, 'formset': formset})


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
    return render(request, 'product_form.html', {'form': form, 'formset': formset})


def product_list(request, pk=None):
    if pk:
        products = Product.objects.filter(category_id=pk).order_by('-created_at')
        selected_category = Category.objects.get(pk=pk)
    else:
        products = Product.objects.all().order_by('-created_at')
        selected_category = None

    context = {
        'products': products,
        'selected_category': selected_category,
    }
    return render(request, 'product_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product.objects.annotate(avg_rating=Avg('reviews__rating')),pk=pk)

    # Get related products (same category, exclude self)
    related_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:6]

    context = {
        'product': product,
        'related_products': related_products,
        'descriptions': product.descriptions.all(),  # get all key-value description entries
        'product_reviews': product.reviews.all()
    }
    return render(request, 'product_detail.html', context)


def rated_products_by_range(request):
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

    return render(request, 'product_list.html', {
        'products': products,
        'min_rating': min_rating,
        'max_rating': max_rating,
    })
