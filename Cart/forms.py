from .models import CartItem
from django import forms

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['items', 'quantity', 'created_at', 'updated_at', 'total_price']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be at least 1.")
        return quantity