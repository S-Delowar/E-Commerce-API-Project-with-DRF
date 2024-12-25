from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from order.models import Order
from rest_framework.test import APITestCase
from rest_framework import status
import stripe, json
from unittest.mock import patch

class PaymentIntegrationTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        
        self.client.force_authenticate(user=self.user)
        
        self.order = Order.objects.create(
            user = self.user,
            total_price = 500,
            status = "pending",
        )
        
    # Test Payment Intent Creation
    def test_create_payment_intent_valid(self):
        response = self.client.post(
            reverse("create-payment-intent"),
            {
                "amount": 1000, 
                "currency": "usd",
                "order_id": self.order.id
            }
        )
        # print(response.status_code)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("client_secret", response.data)
        self.assertIn("payment_intent_id", response.data)
        
    def test_create_payment_intent_invalid_data(self):
        response = self.client.post(
            reverse("create-payment-intent"), {}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # print(response.data)
        self.assertIn("Order not found", response.data["detail"])
        
        
class StripeWebhookTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        
        self.client.force_authenticate(user=self.user)
        
        self.order = Order.objects.create(
            user = self.user,
            total_price = 500,
            status = "pending",
        )
    
    @patch('stripe.Webhook.construct_event')
    def test_webhook_payment_intent_succeeded(self, mock_construct_event):
        mock_event = {
            "type": "payment_intent.succeeded",
            "data": {
                "object": {
                    "metadata": {"order_id": str(self.order.id)}
                }
            }
        }
        mock_construct_event.return_value = mock_event
        
        response = self.client.post(
            reverse('stripe-webhook'),
            data = '{}',
            content_type = 'application/json',
            HTTP_STRIPE_SIGNATURE = 'mock-signature'
        )
        
        self.assertEqual(response.status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "completed")

        
        # sig_header = stripe.Webhook.generate_signature_header(
        #     payload = json.dumps(payload),
        #     secret = settings.STRIPE_WEBHOOK_SECRET_KEY
        # )
        
        # response = self.client.post(
        #     reverse('stripe-webhook'),
        #     data = json.dumps(payload),
        #     content_type = "application/json",
        #     HTTP_STRIPE_SIGNATURE = sig_header
        #     )
        
        # self.assertEqual(response.status_code, 200)
        
        # print("test_webhook_payment_succeeded - okay")