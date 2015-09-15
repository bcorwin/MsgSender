from Factz.do import format_number
#from django_twilio.decorators import twilio_view
from twilio.twiml import Response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def sms_reply(request):
    #str(request.REQUEST)
    r = Response()
    r.message('Hello from your Django app!')
    return HttpResponse(r.toxml(), content_type='text/xml')