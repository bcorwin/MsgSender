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
    from_number = request.REQUEST['From']
    twiml = '<Response><Message>Your number:' + from_number + '</Message></Response>'
    return HttpResponse(twiml, content_type='text/xml')