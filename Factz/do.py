from Factz.models import Variable, Message
from datetime import datetime
from random import choice

def get_value(name):
    return Variable.objects.filter(name=name)
    
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