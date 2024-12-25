from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from order.models import Order
from rest_framework.test import APITestCase
from rest_framework import status


# Create your tests here.


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