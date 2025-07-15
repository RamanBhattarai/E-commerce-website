from django.urls import path
from .views import delivery

urls = [
    path('delivery/', delivery, name='delivery'),
]