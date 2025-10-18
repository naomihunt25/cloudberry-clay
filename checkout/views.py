from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from bag.contexts import bag_contents
import stripe


def checkout(request):
    """Display checkout page and handle Stripe PaymentIntent + order creation."""
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # 🧾 If form submitted (POST) — process the order
    if request.method == 'POST':
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST.get('full_name'),
            'email': request.POST.get('email'),
            'phone_number': request.POST.get('phone_number'),
            'country': request.POST.get('country'),
            'postcode': request.POST.get('postcode'),
            'town_or_city': request.POST.get('town_or_city'),
            'street_address1': request.POST.get('street_address1'),
            'street_address2': request.POST.get('street_address2'),
            'county': request.POST.get('county'),
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.save()

            # Create order line items
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        OrderLineItem.objects.create(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            OrderLineItem.objects.create(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                except Product.DoesNotExist:
                    messages.error(
                        request,
                        "One of the items in your bag wasn’t found. Please contact us!"
                    )
                    order.delete()
                    return redirect(reverse('bag:view_bag'))

            # Save user info preference and redirect to success page
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))

        else:
            messages.error(request, 'There was an issue with your form. Please review your details.')

    # 💡 If GET request — display the checkout page
    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "Your bag is empty at the moment.")
            return redirect(reverse('products:products'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)

        # Configure Stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
            )
        except Exception as e:
            messages.error(request, f"Stripe error: {e}")
            return redirect(reverse('bag:view_bag'))

        order_form = OrderForm()

        if not stripe_public_key:
            messages.warning(request, "Stripe public key is missing. Check your environment variables.")

        # 🪄 Cloudberry-themed checkout context
        context = {
            'order_form': order_form,
            'bag_items': current_bag['bag_items'],
            'total': current_bag['total'],
            'delivery': current_bag['delivery'],
            'grand_total': current_bag['grand_total'],
            'product_count': current_bag['product_count'],
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
        }

        return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    """Handle successful checkouts and show confirmation message."""
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    messages.success(
        request,
        f"Thank you! Your order has been processed successfully. "
        f"Your order number is {order_number}. A confirmation email will be sent to {order.email}."
    )

    # Clear shopping bag
    if 'bag' in request.session:
        del request.session['bag']

    context = {'order': order}
    return render(request, 'checkout/checkout_success.html', context)
