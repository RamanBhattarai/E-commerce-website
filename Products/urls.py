from django.urls import path
from .views import product_create, product_update, product_list, product_detail, product_search, rated_products_by_range

urlpatterns = [
    path('products/', product_list, name='product_list'),
    path('product/create/', product_create, name='product_create'),
    path('products/<int:pk>/', product_detail, name='product_detail'),
    path('products/<int:pk>/edit/', product_update, name='product_update'),
    path('categories/<int:pk>/products/', product_list, name='product_list_by_category'),
    path('products/search/', product_search, name='search'),
    path('products/ratings/', rated_products_by_range, name='rated_products')
]
