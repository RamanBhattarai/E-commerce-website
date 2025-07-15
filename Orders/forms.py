from django import forms
from .models import OrderList

class OrderListForm(forms.ModelForm):
    class Meta:
        model = OrderList
        fields = ['created_at', 'quantity', 'total_price']
        