from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    """Display line items within the Order admin view"""
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)

    extra = 0  # Prevents Django from showing extra blank forms unnecessarily


class OrderAdmin(admin.ModelAdmin):
    """Admin configuration for customer orders"""
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = (
        'order_number', 'date', 'delivery_cost',
        'order_total', 'grand_total', 'original_bag', 'stripe_pid',
    )

    fields = (
        'order_number', 'date', 'full_name', 'email', 'phone_number',
        'country', 'postcode', 'town_or_city', 'street_address1',
        'street_address2', 'county', 'delivery_cost',
        'order_total', 'grand_total', 'original_bag', 'stripe_pid',
    )

    list_display = (
        'order_number', 'date', 'full_name',
        'order_total', 'delivery_cost', 'grand_total',
    )

    ordering = ('-date',)
    search_fields = ('order_number', 'full_name', 'email')


admin.site.register(Order, OrderAdmin)
