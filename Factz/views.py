from django.http import HttpResponse
import twilio.twiml


# Create your views here.
def sms_reply(request):
    out = "<html>"
    dict = request.REQUEST
    for a in request.REQUEST:
        out += a + ":"
        out += dict[a] + "<br>"
    out += "</html>"
    return HttpResponse(out)