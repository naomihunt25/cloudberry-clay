from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    """Form for adding/editing products in the store"""

    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'category',
            'sku',
            'rating',
            'image',
        ]