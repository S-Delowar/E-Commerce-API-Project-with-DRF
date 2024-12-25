from order.models import Order
import stripe 
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET_KEY

@csrf_exempt
def stripe_webhook_view(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Invalid request method"}, status=405)
    
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", None)

    if not sig_header:
        return JsonResponse({"error": "Missing Stripe signature header"}, status=400)
    
    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
        )
        
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            order_id = payment_intent['metadata']['order_id']
            Order.objects.filter(id=order_id).update(status='completed')
            
        elif event['type'] == 'payment_intent.payment_failed':
            payment_intent = event['data']['object']
            order_id = payment_intent['metadata']['order_id']
            Order.objects.filter(id=order_id).update(status='canceled')
        
        return JsonResponse({'status': 'success'}, status=200)
        
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({"error": "Invalid signature"}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    