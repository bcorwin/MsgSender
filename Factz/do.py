#Use do to store functions that may depend on models
from Factz.models import Number, Variable, Message, activeSubscription, Subscription
from datetime import datetime
from random import choice
import csv
from Factz.utils import extract_command
from django.core.exceptions import ValidationError

def get_value(varname):
    return Variable.objects.get(name=varname).val
    
def next_message(subObj, update=True):
    today = datetime.utcnow().date()
    msg_set = Message.objects.all().filter(subscription=subObj, active=True)
    
    min_date = [m.last_sent.date() for m in msg_set if m.last_sent != None]
    min_date = min(min_date) if len(min_date) >0 else today
    ages = [m.last_sent.date() if m.last_sent != None else min_date for m in msg_set]
    ages = [(today - ls).days + 1 for ls in ages]
    
    #randomly select an id given the above weights
    i = int(choice(''.join(str(i)*a for i,a in zip(range(len(msg_set)), ages))))
    res = msg_set[i]
    if update==True:
        res.update_sent()
    return res
    
def number_exist(phone_number):
    """
    If a number is in the database, return it otherwise return None
    """
    num = Number.objects.filter(phone_number=phone_number)
    if num.exists():
        return num.get()
    else:
        return None

def sub_exist(name):
    """
    If a subscription is in the database, return it otherwise return None
    """
    sub = Subscription.objects.filter(name__iexact=name)
    if sub.exists():
        return sub.get()
    else:
        return None
        
def toggle_active(number_id, subscription_id, status=None):
    """
    Either set the active status of a number/subscription pair to status
    or toggle the current status.
    If it does not exist, create it first then activate it.
    Returns the activeSubscription object (asObj)
    """
    asObj = activeSubscription.objects.filter(number=number_id, subscription=subscription_id)
    if not asObj.exists():
        asObj = activeSubscription(number=number_id, subscription=subscription_id)
        status = True
    else:
        asObj = asObj.get()
    asObj.active = status if status != None else not asObj.active
    asObj.save()
    return asObj
    
def add_number(num):
    """
    Adds a number to the database and returns it
    If the number is already in the database the function returns it
    """
    if Number.objects.filter(phone_number=num).exists():
        num = Number.objects.get(phone_number=num)
    else:
        num = Number(phone_number=num)
        num.save()
    return num
    
def upload_file(f, sub, overwrite):
    """
    Reads a csv file (Format: ID, Message, Follow_up, Source) and adds to db.
    """
    out = {"New":[], "Fail":[], "Updated":[], "Nochange":[]}
    if overwrite == True:
        Message.objects.filter(subscription=sub).delete()
    csvreader = csv.reader(f.read().decode().splitlines())
    header = True
    for row in csvreader:
        if header == True:
            header = False
            continue
        sheet_id = int(row[0])
        msg = row[1]
        follow_up = row[2]
        source = row[3]

        msgObj =  Message.objects.filter(sheet_id=sheet_id)
        if msgObj.exists():
            msgObj = msgObj.get()
            changes = {
                "message":find_change(msg, msgObj.message),
                "follow_up":find_change(follow_up, msgObj.follow_up),
                "source":find_change(source, msgObj.source),
            }
            if make_changes(msgObj, changes) == True:
                out = validate_save_append(msgObj, out, name="Updated", addl=changes)
            else:
                out["Nochange"].append(msgObj)
        else:
            add = Message(sheet_id=sheet_id, message=msg, follow_up=follow_up, source=source, subscription=sub)
            out = validate_save_append(add, out)
    return out

def make_changes(obj, changes):
    '''
    Makes changes to obj. If no changes, return False, else return True
    '''
    out = False
    for c in changes:
        if changes[c] != None:
            setattr(obj, c, changes[c][1])
            out = True
    return out

def find_change(new, old):
    '''
    Compares two values. If they are the same, return None. If not return a tuple as (old, new)  
    '''
    return (old, new) if new != old else None
        
def validate_save_append(obj, out, name="New", addl=None):
    '''
    Validates an object. If it's good, save it and return out[name] with an additional entry as (obj, addl).
    If not, return out["Fail"] with an additional entry as (obj, the error)
    '''
    try:
        obj.full_clean()
        obj.save()
        out[name].append((obj, addl))
    except ValidationError as e:
        out["Fail"].append((obj, e))
    return out
    
def generate_reply(message, numObj):
    # To do:
    ## Source [SUB]-- send source for latest message sent
    ## Unsubscribe -- Unsubscribe
    ### Need extract sub(s) from message
    ## Help or Commands -- Send list of available commands
    ## Otherwise do what?
    
    commands = ["subscribe", "unsubscribe"]
    command, parm = extract_command(message, commands)
    
    if command == "subscribe":
        subObj = sub_exist("PoopFactz")
        toggle_active(numObj, subObj, status=True)
        return "You're now subscribed to " + subObj.name + "."
    elif command == "unsubscribe":
        subObj = sub_exist("PoopFactz")
        toggle_active(numObj, subObj, status=False)
        return "You're now unsubscribed to " + subObj.name + "."
    return "Unknown command."
    
def send_to_all(subObj, msgObj=None):
    '''
    Sends a message to all phone numbers with active subscriptions for a given subscription.
    '''
    if msgObj == None:
        msgObj = next_message(subObj)
    user_list = activeSubscription.objects.filter(subscription=subObj, active=True)
    success_cnt = 0
    for user in user_list:
        res = user.send(msgObj)
        if res[0] == 0:
            success_cnt += 1
    if success_cnt > 0:
        msgObj.update_sent()
        subObj.update_sent()
    return success_cnt