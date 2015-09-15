from Factz.do import format_number
#from django_twilio.decorators import twilio_view
#from twilio.twiml import Response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

#@twilio_view
@csrf_exempt
def sms_reply(request):
    #str(request.REQUEST)
    #r = Response()
    #r.message('Hello from your Django app!')
    twiml = '<Response><Message>Hello from your Django app!</Message></Response>'
    return HttpResponse(twiml, content_type='text/xml')