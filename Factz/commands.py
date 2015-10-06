from Factz.do import sub_exist, add_number, number_exist, add_rating
import re

commands = {
            "subscribe":    ["subscribe *(.*)", "add *(.*)"],
            "unsubscribe":  ["unsubscribe *(.*)", "leave *(.*)", "stop *(.*)"],
            "source":       ["source()", "sauce()"],
            "rate":         ["rate *(\d*)", "rating *(\d*)", "(\d+)"]
            }

def extract_command(text, commands):
    '''
    Loops through the list of commands and looks for the pattern
    "COMMAND [PARAMETERS]" and outputs the first match it finds
    '''
    out = [None, None]
    for cname in commands:
        reg_list = commands[cname]
        for reg in reg_list:
            pattern = re.compile(reg, re.IGNORECASE)
            if pattern.match(text):
                parm = pattern.match(text).groups()[0]
                out[0] = cname
                out[1] = parm if parm != '' else None
                print(reg)
                break
    return out
    
def extract_subscription(text):
    '''
    Place older to extract the subscription from a text message
    '''
    return sub_exist("PoopFactz")
    
def subscribe(numObj, subObj):
    '''
    Activate number/subscription in activeSubscription and generate a response
    '''
    numObj.toggle_active(subObj, status=True)
    return "You're now subscribed to " + subObj.name + "."

def unsubscribe(numObj, subObj):
    '''
    Deactivate number/subscription in activeSubscription and generate a response
    '''
    numObj.toggle_active(subObj, status=False)
    return "You're now unsubscribed to " + subObj.name + "."
    
def get_source(numObj):
    '''
    Get the source for the last message and generate a response
    '''
    msgObj = numObj.get_last_message()
    if msgObj is not None:
        return msgObj.source
    else:
        return "You have yet to receive a fact."

def add_user(from_number, message):
    '''
    Add a user to the db and generate a response
    '''
    command, parm = extract_command(message, commands)
    numObj = add_number(from_number)
    subObj = extract_subscription(parm)
    #In future, check that that command == "subscribe"
    numObj.toggle_active(subObj, status=True)
    out = "Welcome to " + subObj.name + "! Your first message is on its way."
    # To do: send last message that was sent for newly subscribed sub?
    return out

def set_rating(numObj, rating):
    '''
    Set the rating and generate a response
    '''
    msgObj = numObj.get_last_message()
    if msgObj is not None:
        rate = add_rating(numObj, msgObj, rating)
        if rate == None:
            return "Thanks for the rating!"
        else:
            return "Please submit a rating 1 through 5."
    else:
        return "You have yet to receive a fact."
        
def update_user(message, numObj):
    '''
    Use this for a number already in the db.
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
        out = get_source(numObj)
    elif command == "rate":
        out = set_rating(numObj, parm)
    else:
        out = "Unknown command. "
        out += "Try one of these: "
        out += ", ".join(commands)
    return out
    
def gen_reply(from_number, message):
    '''
    High level function to generate a reply to a text
    '''
    numObj = number_exist(from_number)
    if numObj == None:
        reply = add_user(from_number, message)
    else:
        reply = update_user(message, numObj)
    return reply
    