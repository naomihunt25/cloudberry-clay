from django.urls import path
from . import views
from .webhooks import webhook

app_name = 'checkout'

urlpatterns = [
    # Checkout page
    path('', views.checkout, name='checkout'),

    # Checkout success page
    path('checkout_success/<order_number>/', views.checkout_success, name='checkout_success'),

    # Stripe cache checkout data endpoint
    path('cache_checkout_data/', views.cache_checkout_data, name='cache_checkout_data'),

    # Stripe webhook endpoint
    path('wh/', webhook, name='webhook'),
]
