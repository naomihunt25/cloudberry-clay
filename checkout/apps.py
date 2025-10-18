from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    """
    App config for the Checkout app.
    This makes sure our signals are loaded when the app starts.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'

    def ready(self):
        # Import signals to keep order totals updated automatically
        import checkout.signals