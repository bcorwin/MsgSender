#Use do to store functions that may depend on models
from Factz.models import Number, Variable, Message, activeSubscription, Subscription
from datetime import datetime
from random import choice
import csv
from django.core.exceptions import ValidationError
from Factz.utils import extract_command

def get_value(varname):
    return Variable.objects.get(name=varname).val
    
def next_message(subObj):
    today = datetime.utcnow().date()
    msg_set = Message.objects.all().filter(subscription=subObj, active=True)
    
    min_date = [m.last_sent.date() for m in msg_set if m.last_sent != None]
    min_date = min(min_date) if len(min_date) >0 else today
    ages = [m.last_sent.date() if m.last_sent != None else min_date for m in msg_set]
    ages = [(today - ls).days + 1 for ls in ages]
    
    #randomly select an id given the above weights
    i = int(choice(''.join(str(i)*a for i,a in zip(range(len(msg_set)), ages))))
    res = msg_set[i]
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
    if overwrite == True:
        Message.objects.filter(subscription=sub).delete()
    csvreader = csv.reader(f.read().decode().splitlines())
    header = True
    for row in csvreader:
        if header == True:
            header = False
            continue
        msg = row[1]
        follow_up = row[2]
        source = row[3]
        add = Message(message=msg, follow_up=follow_up, source=source, subscription=sub)
        add.save()
        
def generate_reply(message, numObj):
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
        print(res)
    if success_cnt > 0:
        msgObj.update_sent()
        subObj.update_sent()
    return success_cnt