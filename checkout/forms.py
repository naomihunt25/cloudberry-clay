from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Order


class OrderForm(forms.ModelForm):
    """Form for users to enter their checkout and delivery details."""

    class Meta:
        model = Order
        fields = (
            'full_name', 'email', 'phone_number',
            'street_address1', 'street_address2',
            'town_or_city', 'postcode', 'country', 'county',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Crispy form setup
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'checkout-form bg-white p-3 shadow-sm rounded'
        self.helper.add_input(Submit('submit', 'Place Order',
            css_class='btn text-white rounded-pill px-4 py-2',
            style='background-color: var(--accent-blue); border: none;'))

        # Placeholders for each field
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
        }

        # Focus on first field
        self.fields['full_name'].widget.attrs['autofocus'] = True

        # Add placeholders + styling
        for field in self.fields:
            placeholder = placeholders[field]
            if self.fields[field].required:
                placeholder += ' *'
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False