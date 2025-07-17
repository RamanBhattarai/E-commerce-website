from .models import DeliveryList
from django import forms

class DeliveryListForm(forms.ModelForm):
    class Meta:
        model = DeliveryList
        fields = ['delivery_address', 'delivery_method']

