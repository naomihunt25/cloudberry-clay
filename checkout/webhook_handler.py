from django.http import HttpResponse

class StripeWH_Handler:
    """Handles Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """Handle a general or unknown webhook event"""
        return HttpResponse(
            content=f"Unhandled event type: {event['type']}",
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """Handle successful payment intent from Stripe"""
        intent = event.data.object
        pid = intent.id
        print(f"Payment succeeded for {pid}")

        return HttpResponse(
            content=f"Webhook received: {event['type']} | SUCCESS: {pid}",
            status=200
        )

    def handle_payment_intent_payment_failed(self, event):
        """Handle failed payment intent from Stripe"""
        intent = event.data.object
        print(f"Payment failed for {intent.id}")

        return HttpResponse(
            content=f"Webhook received: {event['type']} | FAILED",
            status=200
        )