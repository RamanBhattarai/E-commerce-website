from django.urls import path
from . import views

urlpatterns = [
    path('checkout/<str:order_number>/', views.checkout, name='checkout'),
    path('khalti-verify/', views.khalti_verify, name='khalti_verify'),
    path('success/', views.payment_success, name='payment_success'),
    path('payment_method/<str:order_number>/', views.payment_method, name='payment_method'),
]