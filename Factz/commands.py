from Factz.models import activeSubscription
from Factz.do import toggle_active, sub_exist
import re

def extract_command(text, commands):
    """
    Loops through the list of commands and looks for the pattern
    "COMMAND [PARAMETERS]" and outputs the first match it finds
    """
    out = [None, None]
    for c in commands:
        pattern = re.compile(c + " *(.*)", re.IGNORECASE)
        if pattern.match(text):
            parm = pattern.match(text).groups()[0]
            out[0] = c
            out[1] = parm if parm != '' else None
            break
    return out
    
def subscribe(numObj, subObj):
    toggle_active(numObj, subObj, status=True)
    return "You're now subscribed to " + subObj.name + "."

def unsubscribe(numObj, subObj):
    toggle_active(numObj, subObj, status=False)
    return "You're now unsubscribed to " + subObj.name + "."
    
def get_source(numObj, subObj):
    asObj = activeSubscription.objects.filter(number=numObj, subscription=subObj)
    if asObj.exists():
        asObj = asObj.get()
        if asObj.message is not None:
            return asObj.message.source
        else:
            return "You have yet to recieve a fact from " + subObj.name + "."
    else:
        return "You are not subscribed to " + subObj.name + "."

def generate_reply(message, numObj):
    '''
    Generate the reply to a text message given the message, list of commands,
    and number object.
    '''
    
    commands = ["subscribe", "unsubscribe", "source"]
    command, parm = extract_command(message, commands)
    
    subObj = sub_exist("PoopFactz")    
    
    if command == "subscribe":
        out = subscribe(numObj, subObj)
    elif command == "unsubscribe":
        out = unsubscribe(numObj, subObj)
    elif command == "source":
        out = get_source(numObj, subObj)
    else:
        out = "Unknown command."
    return out