from django.contrib import admin
from .models import UserProfile

# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'full_name', 'address', 'phone_number', 'date_joined')
    search_fields = ('username', 'email', 'fullname', 'phone_number')
    ordering = ('-date_joined',)