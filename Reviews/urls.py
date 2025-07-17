from django.urls import path
from .views import rated_products_by_range

urlpatterns = [
    path('rated/', rated_products_by_range, name='rated_products'),
]
