import twilio
from twilio.rest import TwilioRestClient
from do import get_value
from Factz.models import Message, Number

def send_text(message, to_number, from_number=get_value("twilio_live_number"), account_sid=get_value("twilio_live_sid"), auth_token=get_value("twilio_live_token")):
    # Low level function to send text messagaes using Twilio, sends using live keys by default
    try: 
        client = TwilioRestClient(account_sid, auth_token)
        sms = client.sms.messages.create(body=message, to=to_number, from_=from_number)
        out = (0, "Success")
    except twilio.TwilioRestException as e:
        out = (e.code, e.msg)
    # To do: catch unknown errors too
    return(out)
    
def send_message(message_id, number_id, *args, **kwargs):
    # Send a message to a number based on message and number ids.
    msg = Message.objects.filter(id=message_id).message
    to_number = Number.objects.filter(id=number_id).number
    
    out = send_text(msg, to_number, *args, **kwargs)
    return(out)

def send_test_message(message_id=None, message_text=None, number_id=None, to_number=None):
    # 'Sends' a message using the test api so it does not cost money. Use this to validate numbers
    if message_id == None and message_text == None:
        raise ValueError("Please provide at least message_id or message_text.")
    elif message_id != None:
        msg = Message.objects.filter(id=message_id).message
        
    if number_id == None and to_number == None:
        raise ValueError("Please provide at least number_id or to_number.")
    elif number_id != None:
        to_number = Number.objects.filter(id=number_id).number
    
    from_number=get_value("twilio_test_number")
    account_sid=get_value("twilio_test_sid")
    auth_token=get_value("twilio_test_token")
    
    out = send_text(message_text, to_number, from_number, account_sid, auth_token)
    return(out)
    
def send_confirmation_code(number_id, *args, **kwargs):
    # Sends the confirmation code using the number id
    msg = "Thank you for subscribing to PoopFactz. Your confirmation code is "
    msg += Number.objects.filter(id=number_id).confirmation_code
    msg += ". Go to www.PoopFactz.com/Subscribe to recieve your message."
    to_number = Number.objects.filter(id=number_id).number
    
    out = send_text(msg, to_number, *args, **kwargs)
    return(out)