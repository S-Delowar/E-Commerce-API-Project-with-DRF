from django.urls import path

from payment.payment_intent import CreatePaymentIntentView


urlpatterns = [
    path('payment-intent', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    
]
