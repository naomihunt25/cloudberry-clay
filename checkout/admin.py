from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemInline(admin.TabularInline):
    """
    Lets us see and edit line items right inside the order page.
    """
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)  # show total but don’t let it be edited


class OrderAdmin(admin.ModelAdmin):
    """
    Custom admin view for Cloudberry Clay orders.
    """
    inlines = (OrderLineItemInline,)

    # Fields that shouldn’t be changed manually
    readonly_fields = (
        'order_number',
        'date',
        'delivery_cost',
        'order_total',
        'grand_total',
    )

    # Order in which fields appear in the admin form
    fields = (
        'order_number', 'date', 'full_name', 'email',
        'phone_number', 'country', 'postcode', 'town_or_city',
        'street_address1', 'street_address2', 'county',
        'delivery_cost', 'order_total', 'grand_total',
    )

    # What shows up in the list view in the admin
    list_display = (
        'order_number',
        'date',
        'full_name',
        'order_total',
        'delivery_cost',
        'grand_total',
    )

    ordering = ('-date',)  # newest orders first


# finally, register it so it appears in the admin site
admin.site.register(Order, OrderAdmin)