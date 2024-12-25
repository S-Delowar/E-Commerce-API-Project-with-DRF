import stripe 
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.Meta.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.WEBHOOK_SECRET_KEY
    
    pass