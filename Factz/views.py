from Factz.utils import format_number
from Factz.do import confirm_code, number_exist
from django_twilio.decorators import twilio_view
from twilio.twiml import Response
from Factz.models import Number
from django.http import HttpResponse
from django.db import IntegrityError

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
    
def signup(request):
    if request.method == "POST":
        num = request.POST['Number']
    elif request.method == "GET":
        num = request.GET['Number']
        
    try:
        num = format_number(num)
    except ValueError:
        return HttpResponse("Please enter a number in the format 555 555 5555.")
    
    try:
        new = Number(phone_number=num)
        new.save()
    except IntegrityError:
        return HttpResponse("You're already signed up!")
    
    return HttpResponse("Thanks for signing up! Your confirmation code is on its way.")
    
def confirm(request):
    if request.method == "POST":
        num = request.POST['Number']
        code = request.POST['Code']
    elif request.method == "GET":
        num = request.GET['Number']
        code = request.GET['Code']
    try:
        num = format_number(num)
    except ValueError:
        return HttpResponse("Please enter a number in the format 555 555 5555.")
        
    if number_exist(num):
        out = confirm_code(code, phone_number=num)
    else:
        out = "You have not signed up. Please go to <a href='www.PoopFactz.com/signup'>www.PoopFactz.com/signup</a> to get started."
    return HttpResponse(out)