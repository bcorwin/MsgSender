from Factz.utils import format_number
from Factz.do import number_exist, add_number, toggle_active, sub_exist, upload_file, generate_reply, send_to_all, next_message
from Factz.forms import uploadFactz, sendForm
from django_twilio.decorators import twilio_view
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template.context_processors import csrf
from twilio.twiml import Response

@twilio_view
def sms_reply(request):
    if request.method == "POST":
        from_number = format_number(request.POST['From'])
        msg = request.POST['Body']
    elif request.method == "GET":
        from_number = format_number(request.GET['From'])
        msg = request.GET['Body']
        
    r = Response()
    numObj = number_exist(from_number)
    if numObj == None:
        numObj = add_number(from_number)
        # To do: look for "subscribe {SUB}" pattern
        subObj = sub_exist("PoopFactz")
        toggle_active(numObj, subObj, status=True)
        r.message("Welcome to PoopFactz! Your first message is on its way.")
        # To do: send last message that was sent for newly subscribed sub?
    else:
        reply = generate_reply(msg, numObj)
        r.message(reply)
    return r
    
@twilio_view
def voice(request):
    r = Response()
    #subObj = sub_exist("PoopFactz")
    #msgObj = next_message(subObj, update=False)
    
    #r.say(msgObj.message)
    #if msgObj.follow_up != None:
    #    r.pause(length=2)
    #    r.say(msgObj.follow_up)
    #r.pause(length=2)
    #r.say("Thank you for calling Poop Facts. To subscribe for daily text message go to www dot Poop Facts dot com.")
    #r.pause(length=1)
    #r.say("That's Poop Facts with a zee")
    
    # To do:
    ## Have the caller press 1 to subscribe to PoopFactz
    
    r.reject()
    return r
    
@staff_member_required
def upload(request):
    if request.method == 'POST':
        form = uploadFactz(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            upload_file(request.FILES['file'], sub=cd['subscription'], overwrite=cd['overwrite'])
            return HttpResponse("Success")
        return HttpResponse("Fail" + str(form.errors))
    else:
        form = uploadFactz
    out = {'form': form}
    out.update(csrf(request))
    return render_to_response('upload.html', out)
    
@staff_member_required
def send(request):
    if request.method == 'POST':
        form = sendForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            sub = cd['subscription']
            msg = cd['message']
            if msg != None:
                if msg.subscription != sub:
                    return HttpResponse("Fail. Be sure to select a message that is for the selected subscription")
            send_to_all(sub, msgObj=msg)
            return HttpResponse("Success")
        return HttpResponse("Fail" + str(form.errors))
    else:
        form = sendForm
    out = {'form': form}
    out.update(csrf(request))
    return render_to_response('send.html', out)
    
@staff_member_required
def home(request):
    out ={
        'menu':{
            "Admin": "/admin",
            "Send to all":"/send",
            "Upload":"/upload",
        }
    }
    return render_to_response('home.html', out)