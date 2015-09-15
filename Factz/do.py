from datetime import datetime
from random import choice, sample
import re

def rand_code():
    code = sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 2) + sample('1234567890', 4)
    return ''.join(code)

def get_value(varname):
    from Factz.models import Variable
    return Variable.objects.get(name=varname).val
    
def next_message(subscription_id):
    from Factz.models import Message
    today = datetime.now().date()
    msg_set = Message.objects.all().filter(subscription_id=subscription_id)
    msg_set = msg_set.filter(active=True)
    ids = [m.id for m in msg_set]
    
    min_date = min([m.last_sent.date() for m in msg_set if m.last_sent != None])
    ages = [m.last_sent.date() if m.last_sent != None else min_date for m in msg_set]
    ages = [(today - ls).days for ls in ages]
    
    #randomly select an id given the above weights
    return int(choice(''.join(str(i)*a for i,a in zip(ids, ages))))
    
def format_number(phone_number):
    phone_number = str(phone_number)
    phonePattern = re.compile(r'^\D*\+{0,1}1{0,1}\D*(\d{3})\D*(\d{3})\D*(\d{4}).*$', re.VERBOSE)
    if phonePattern.match(phone_number):
        grps = phonePattern.search(phone_number).groups()
        out = "+1" + ''.join(grps[0:3])
    else:
        raise ValueError(phone_number + " is not a valid phone number format.")
    return(out)
    
def lookup_number(number):
    from Factz.models import Number
    