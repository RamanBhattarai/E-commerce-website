from django.urls import path
from .views import cart_view, add_to_cart, clear_cart, remove_from_cart, add_quantity, subtract_quantity, wishlist

urlpatterns = [
    path('cart/', cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/', clear_cart, name='clear_cart'),
    path('cart/remove/<int:item_id>', remove_from_cart, name='remove_from_cart'),
    path('cart/add/<int:product_id>/add', add_quantity, name='add_quantity'),
    path('cart/add/<int:product_id>/subtract', subtract_quantity, name='subtract_quantity'),
    path('wishlist/', wishlist, name='wishlist')
]