from Factz.do import toggle_active, sub_exist, add_number, number_exist, get_activeSub
import re

commands = ["subscribe", "unsubscribe", "source"]

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
    
def extract_subscription(text):
    return sub_exist("PoopFactz")
    
def subscribe(numObj, subObj):
    toggle_active(numObj, subObj, status=True)
    return "You're now subscribed to " + subObj.name + "."

def unsubscribe(numObj, subObj):
    toggle_active(numObj, subObj, status=False)
    return "You're now unsubscribed to " + subObj.name + "."
    
def get_source(numObj, subObj):
    asObj = get_activeSub(numObj, subObj)
    if asObj.exists():
        asObj = asObj.get()
        if asObj.message is not None:
            return asObj.message.source
        else:
            return "You have yet to recieve a fact from " + subObj.name + "."
    else:
        return "You are not subscribed to " + subObj.name + "."

def add_user(from_number, message):
    command, parm = extract_command(message, commands)
    numObj = add_number(from_number)
    subObj = extract_subscription(parm)
    #In future, check that that command == "subscribe"
    toggle_active(numObj, subObj, status=True)
    out = "Welcome to PoopFactz! Your first message is on its way."
    # To do: send last message that was sent for newly subscribed sub?
    return out

def update_user(message, numObj):
    '''
    Generate the reply to a text message given the message, list of commands,
    and number object.
    '''
    command, parm = extract_command(message, commands)
    
    subObj = extract_subscription(parm)
    
    if command == "subscribe":
        out = subscribe(numObj, subObj)
    elif command == "unsubscribe":
        out = unsubscribe(numObj, subObj)
    elif command == "source":
        out = get_source(numObj, subObj)
    else:
        out = "Unknown command."
    return out
    
def gen_reply(from_number, message):
    numObj = number_exist(from_number)
    if numObj == None:
        reply = add_user(from_number, message)
    else:
        reply = update_user(message, numObj)
    return reply
    