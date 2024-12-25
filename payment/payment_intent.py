from order.models import Order
import stripe
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound


stripe.api_key = settings.STRIPE_SECRET_KEY

class CreatePaymentIntentView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def post(self, request):
        try:
            order_id = request.data.get('order_id')
            order = Order.objects.get(id=order_id, user=request.user)
            
            intent = stripe.PaymentIntent.create(
                amount = int(order.total_price * 100),
                currency = 'usd',
                metadata = {'order_id': order.id},
            )
            
            return Response({
                'client_secret': intent['client_secret'],
                'payment_intent_id': intent['id']
            }, status=200)
        
        except Order.DoesNotExist:
            raise NotFound('Order not found')
        except Exception as e:
            return Response({
                'detail': str(e)
            }, status=500)












