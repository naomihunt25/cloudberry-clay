from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):
    """
    Makes the shopping bag contents available across all templates.
    Includes free delivery logic for orders over £50.
    """
    bag_items = []
    total = Decimal('0.00')
    product_count = 0
    bag = request.session.get('bag', {})

    # Build up bag items
    for item_id, quantity in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        item_total = quantity * product.price
        total += item_total
        product_count += quantity
        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
            'subtotal': item_total,
        })

    # Free delivery threshold (you can also define this in settings.py)
    FREE_DELIVERY_THRESHOLD = getattr(settings, 'FREE_DELIVERY_THRESHOLD', 50)
    STANDARD_DELIVERY_PERCENTAGE = getattr(settings, 'STANDARD_DELIVERY_PERCENTAGE', 10)

    # Delivery logic
    if total < FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = Decimal('0.00')
        free_delivery_delta = Decimal('0.00')

    grand_total = total + delivery

    # Context passed to all templates
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context