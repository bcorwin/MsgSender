from django.http import HttpResponse
from Factz.models import Number
from Factz.do import format_number
import twilio.twiml


# Create your views here.
def sms_reply(request):
    out = "<html>"
    dict = request.REQUEST
    for a in request.REQUEST:
        out += a + ":"
        out += dict[a] + "<br>"
        
    try:
        from_number = dict["From"]
        from_number = format_number(from_number)
        cc = Number.objects.get(phone_number=from_number).phone_number
        out += "<br>Your confirmation code: " + cc
    except:
        out += "<br>Number is not valid."
    finally:
        out += "</html>"
    return HttpResponse(out)