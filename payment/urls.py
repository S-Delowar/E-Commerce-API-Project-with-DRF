from django.urls import path

from payment.payment_intent import CreatePaymentIntentView
from payment.webhooks import stripe_webhook_view


urlpatterns = [
    path('payment-intent', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    path('payment-intent/stripe', CreatePaymentIntentView.as_view(), name='create-payment-intent'),

    path('webhook/', stripe_webhook_view, name='stripe-webhook'),    
]
