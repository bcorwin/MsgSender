#Do not write functions that depend on models
import twilio
from twilio.rest import TwilioRestClient
from django.conf import settings
from time import sleep

def send_test_message(numObj):
    """
    'Sends' a message using the test api so it does not cost money. Use this to validate numbers
    """
    to_number = numObj.phone_number
    
    from_number= settings.TWILIO_TEST_NUMBER
    account_sid= settings.TWILIO_TEST_SID
    auth_token = settings.TWILIO_TEST_TOKEN
    
    out = send_text("Test.", to_number, from_number, account_sid, auth_token)
    return(out)

def send_message(msgObj, asObj, type="message"):
    '''
    Send a message to a number based on message and number ids.
    '''
    type = type[0].upper()
    if type == "M":
        msg = msgObj.message
    elif type == "F":
        msg = msgObj.follow_up
    elif type == "S":
        msg = msgObj.source
    else:
        return (3, "Invalid type")
        
    to_number = asObj.number.phone_number
    out = send_text(message=msg, to_number=to_number)
    return(out)
    
def send_text(message, to_number, from_number=settings.TWILIO_LIVE_NUMBER, account_sid=settings.TWILIO_ACCOUNT_SID, auth_token=settings.TWILIO_AUTH_TOKEN):
    '''
    Low level function to send text messages using Twilio, sends using live keys by default
    '''
    try:
        client = TwilioRestClient(account_sid, auth_token)
        sms = client.messages.create(body=message, to=to_number, from_=from_number)
        out = (0, "Success")
        if from_number == settings.TWILIO_TEST_NUMBER:
            print(sms.to + ":" + sms.body)
        sleep(1)
    except twilio.TwilioRestException as e:
        out = (e.code, e.msg)
    except:
        out = (1, "Unknown error")
    return(out)