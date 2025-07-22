from django.urls import path
from . import views

urlpatterns = [
    path('submit-review/<int:pk>/', views.submit_review, name='submit_review'),
]