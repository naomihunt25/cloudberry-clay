from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'full_name',
            'email',
            'phone_number',
            'street_address1',
            'street_address2',
            'town_or_city',
            'postcode',
            'country',
            'county',
        )

    def __init__(self, *args, **kwargs):
        """
        Add placeholders, CSS classes, and remove labels.
        Set autofocus on the first field for better UX.
        """
        super().__init__(*args, **kwargs)

        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Postcode',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
        }

        # Autofocus the first field
        self.fields['full_name'].widget.attrs['autofocus'] = True

        for field in self.fields:
            if field != 'country':
                # Add placeholder text
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder

            # Add common CSS classes
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            # Hide labels for cleaner layout
            self.fields[field].label = False

        # Improve country dropdown styling
        self.fields['country'].widget.attrs['class'] = 'stripe-style-input'
