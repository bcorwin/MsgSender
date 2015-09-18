from Factz.models import Number, Variable, Message, activeSubscription, Subscription
from datetime import datetime
from random import choice

def get_value(varname):
    return Variable.objects.get(name=varname).val
    
def next_message(subscription_id):
    today = datetime.now().date()
    msg_set = Message.objects.all().filter(subscription=subscription_id)
    msg_set = msg_set.filter(active=True)
    
    min_date = min([m.last_sent.date() for m in msg_set if m.last_sent != None])
    ages = [m.last_sent.date() if m.last_sent != None else min_date for m in msg_set]
    ages = [(today - ls).days for ls in ages]
    
    #randomly select an id given the above weights
    i = int(choice(''.join(str(i)*a for i,a in zip(range(len(msg_set)), ages))))
    return msg_set[i]
    
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