from Factz.utils import format_number
from Factz.do import number_exist, add_number, toggle_active, sub_exist, upload_file, generate_reply
from django_twilio.decorators import twilio_view
from twilio.twiml import Response
from Factz.forms import uploadFactz
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template.context_processors import csrf

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
    else:
        reply = generate_reply(msg, numObj)
        r.message(reply)
    # To do:
    ## Check if number in DB.
    ### If not: if msg contains subscribe SUB, subscribe and activate them
    ### If in, look for:
    #### Source [SUB]-- send source for latest message sent
    #### Unsubscribe -- Unsubscribe
    #### More -- Tell them to wait
    #### Help or Commands -- Send list of available commands
    #### Otherwise send list of commands
    return r
    
@twilio_view
def voice(request):
    r = Response()
#    subObj = sub_exist("PoopFactz")
#    msgObj = next_message(subObj)
#    
#    r.say(msgObj.message)
#    if msgObj.follow_up != None:
#        r.pause(length=2)
#        r.say(msgObj.follow_up)
#    r.pause(length=2)
#    r.say("Thank you for calling Poop Facts. To subscribe for daily text message go to www. Poop Facts .com")
#    r.pause(length=1)
#    r.say("Thats Poop Facts with a zee")
    
    # To do:
    ## Play a random message
    ## Have the caller press 1 to subscribe to PoopFactz
    
    r.reject()
    return r
    
def upload(request):
    if request.method == 'POST':
        form = uploadFactz(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            upload_file(request.FILES['file'], sub=cd['subscription'], overwrite=cd['overwrite'])
            return HttpResponse("Success")
        return HttpResponse("Fail")
    else:
        form = uploadFactz
    out = {'form': form}
    out.update(csrf(request))
    return render_to_response('upload.html', out)