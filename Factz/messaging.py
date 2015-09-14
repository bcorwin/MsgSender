import twilio
from twilio.rest import TwilioRestClient
from Factz.do import get_value

def send_text(message, to_number, from_number=None, account_sid=None, auth_token=None):
    # Low level function to send text messages using Twilio, sends using live keys by default
    if from_number == None: from_number=get_value("twilio_live_number")
    if account_sid == None: account_sid=get_value("twilio_live_sid")
    if auth_token == None: auth_token=get_value("twilio_live_token")
    try:
        client = TwilioRestClient(account_sid, auth_token)
        sms = client.sms.messages.create(body=message, to=to_number, from_=from_number)
        out = (0, "Success")
    except twilio.TwilioRestException as e:
        out = (e.code, e.msg)
    except:
        out = (0, "Unknown error")
    return(out)
    
def send_message(message_id, number_id, *args, **kwargs):
    from Factz.models import Message, Number
    # Send a message to a number based on message and number ids.
    msg = Message.objects.get(pk=message_id).message
    to_number = Number.objects.get(pk=number_id).phone_number
    
    out = send_text(msg, to_number, *args, **kwargs)
    return(out)
        
def send_test_message(number_id=None, to_number=None):
    # 'Sends' a message using the test api so it does not cost money. Use this to validate numbers
    if number_id == None and to_number == None:
        raise ValueError("Please provide at least number_id or to_number.")
    elif number_id != None:
        to_number = Number.objects.get(id=number_id).phone_number
    
    from_number=get_value("twilio_test_number")
    account_sid=get_value("twilio_test_sid")
    auth_token=get_value("twilio_test_token")
    
    out = send_text("Test.", to_number, from_number, account_sid, auth_token)
    return(out)
    
def send_confirmation_code(number_id, *args, **kwargs):
    from Factz.models import Number
    # Sends the confirmation code using the number id
    msg = "Thank you for subscribing to PoopFactz. Your confirmation code is "
    msg += Number.objects.get(pk=number_id).confirmation_code
    msg += ". Go to www.PoopFactz.com/Subscribe to recieve your message."
    to_number = Number.objects.get(pk=number_id).phone_number
    
    out = send_text(msg, to_number, *args, **kwargs)
    return(out)