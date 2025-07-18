from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import UserProfile
from .edit_form import UserProfileEditForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, logout
from Orders.models import Order
from django.contrib import messages


# Create your views here.
@login_required(login_url='login')
def profile_view(request):
    user_profile = get_object_or_404(UserProfile, username=request.user.username)
    user_orders = Order.objects.filter(user=request.user, status='pending')
    return render(request, 'Users/profile_view.html', {
        'profile': user_profile,
        'order': user_orders
    })


@login_required(login_url='login')
def edit_profile_view(request):
    user_profile = UserProfile.objects.get(username=request.user.username)
    
    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileEditForm(instance=user_profile)
    
    return render(request, 'Users/edit_profile_view.html', {'form': form})


@login_required(login_url='login')
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # prevents logout after password change
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'Users/change_password.html', {'form': form})


@login_required(login_url='login')
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        messages.success(request, "Your account has been successfully deleted.")
        return redirect('home')
    else:
        return redirect('profile')  # Disallow GET access
