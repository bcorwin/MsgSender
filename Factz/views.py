from Factz.do import format_number
from django_twilio.decorators import twilio_view
from twilio.twiml import Response
from Factz.models import Number

@twilio_view
def sms_reply(request):
    if request.method == "POST":
        from_number = format_number(request.POST['From'])
    elif request.method == "GET":
        from_number = format_number(request.GET['From'])
        
    r = Response()
    try:
        cc = Number.objects.get(phone_number=from_number).confirmation_code
        r.message("Your confirmation code: " + cc)
    except:
        r.message("To sign up for PoopFactz go to www.PoopFactz.com")
    return r
    
@twilio_view
def voice(request):
    r = Response()
    
    r.reject()
    return r