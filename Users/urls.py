from django.urls import path
from .views import profile_view, edit_profile_view, change_password_view, delete_profile

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('profile/change-password/', change_password_view, name='change_password'),
    path('profile/delete/', delete_profile, name='delete_account'),
]