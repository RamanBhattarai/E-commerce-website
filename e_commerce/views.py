# home/views.py
from django.shortcuts import render, redirect, get_object_or_404
from Products.models import Product, Category  # import from the correct app
from django.utils.timezone import now
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model



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


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('BlogPostList')
        else:
            return HttpResponse("Invalid credentials", status=401)
    return render(request, 'login.html')


User = get_user_model()

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists", status=400)

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        # Authenticate and login the user automatically
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # ✅ Auto-login
            return redirect('Home')

    return render(request, 'register.html')


@login_required(login_url='login')
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('Home')