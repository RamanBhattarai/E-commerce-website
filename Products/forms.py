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
       

ProductDescriptionFormSet = inlineformset_factory(
    Product, ProductDescription,
    fields=('key', 'value'),
    extra=1,
    can_delete=True
)