from django.urls import path
from .views import order_view, place_order, order_details_view, cancel_order, order_history, invoice_generation

urlpatterns = [
    path('order/', order_view, name='order_view'),
    path('order_details_view/<str:order_number>/', order_details_view, name='order_details_view'),
    path('order_history/', order_history, name='order_history'),
    path('order/add/', place_order, name='place_order'),
    path('order/remove/<str:order_number>/', cancel_order, name='cancel_order'),
    path('order/<str:order_number>/invoice/', invoice_generation, name='invoice_generation')
]