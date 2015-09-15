from django.http import HttpResponse
from Factz.models import Number
from Factz.do import format_number
import twilio.twiml


# Create your views here.
def sms_reply(request):
    resp = twilio.twiml.Response()
    resp.message(str(request.REQUEST))
    return HttpResponse(resp.toxml(), content_type="text/xml")