from Factz.do import format_number
#from django_twilio.decorators import twilio_view
from twilio.twiml import Response
from django.views.decorators.csrf import csrf_exempt
from Factz.models import Number

#@twilio_view
@csrf_exempt
def sms_reply(request):
    from_number = format_number(request.POST["From"])
    cc = Number.objects.get(phone_number=from_number).confirmation_code
    r = Response()
    r.message('Your confirmation: ' + cc)
    return r