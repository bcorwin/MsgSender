from Factz.models import Number, Variable, Message
from datetime import datetime
from random import choice

def get_value(varname):
    return Variable.objects.get(name=varname).val
    
def next_message(subscription_id):
    today = datetime.now().date()
    msg_set = Message.objects.all().filter(subscription_id=subscription_id)
    msg_set = msg_set.filter(active=True)
    ids = [m.id for m in msg_set]
    
    min_date = min([m.last_sent.date() for m in msg_set if m.last_sent != None])
    ages = [m.last_sent.date() if m.last_sent != None else min_date for m in msg_set]
    ages = [(today - ls).days for ls in ages]
    
    #randomly select an id given the above weights
    return int(choice(''.join(str(i)*a for i,a in zip(ids, ages))))
    
def confirm_code(confirmation_code, phone_number=None, number_id=None):
    # Checks if the submitted confirmation_code matches the one in the DB for the given phone_number
    ## To do: add error checking
    if phone_number == None and number_id == None:
        raise ValueError("Need at least phone_number or number_id.")
    elif number_id == None:
        number_id = Number.objects.get(phone_number=phone_number).pk
    
    numObj = Number.objects.get(pk=number_id)
    
    if numObj.confirmation_code == confirmation_code:
        numObj.confirmed = True
        numObj.save()
        
    return numObj.confirmed
    
def number_exist(phone_number):
    return Number.objects.filter(phone_number=phone_number).exists()