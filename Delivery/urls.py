from django.urls import path
from .views import delivery

urlpatterns = [
    path('delivery/', delivery, name='delivery'),
]
