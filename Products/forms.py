from django import forms
from .models import Product, Category, ProductDescription
from django.forms.models import inlineformset_factory


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'brand', 'price', 'category', 'stock_count', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter product name'}),
            'brand': forms.TextInput(attrs={'placeholder': 'Brand'}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'stock_count': forms.NumberInput(),
            'status': forms.Select(),
        }
        labels = {
            'stock_count': 'Available Stock',
        }
        help_texts = {
            'image': 'Upload a clear image (JPEG/PNG).',
        }


ProductDescriptionFormSet = inlineformset_factory(
    Product, ProductDescription,
    fields=('key', 'value'),
    extra=1,
    can_delete=True
)