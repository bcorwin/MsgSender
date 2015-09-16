from Factz.do import format_number
#from django_twilio.decorators import twilio_view
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Factz.models import Number

#@twilio_view
@csrf_exempt
def sms_reply(request):
    if request.method == "POST":
        from_number = format_number(request.POST['From'])
    elif request.method == "GET":
        from_number = format_number(request.GET['From'])
        
    try:
        cc = Number.objects.get(phone_number=from_number).confirmation_code
        twiml = '<Response><Message>Your confirmation code:' + cc + '</Message></Response>'
    except:
        twiml = '<Response><Message>To sign up for PoopFactz go to www.PoopFactz.com</Message></Response>'
    return HttpResponse(twiml, content_type='text/xml')