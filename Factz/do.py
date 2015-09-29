#Use do to store functions that may depend on models
from Factz.models import Number, Variable, Message, activeSubscription, Subscription
from datetime import datetime
from random import choice
import csv
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from time import sleep

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
    
def send_to_all(subObj, msgObj=None):
    '''
    Sends a message to all phone numbers with active subscriptions for a given subscription.
    '''
    texts = []
    if msgObj == None:
        msgObj = next_message(subObj)
    user_list = activeSubscription.objects.filter(subscription=subObj, active=True)
    success_cnt = 0
    for user in user_list:
        add = {"Number":user}
        res = user.send_message(msgObj)
        if res["Message"][0] == 0:
            success_cnt += 1
        add.update(res)
        texts.append(add)
    if success_cnt > 0:
        msgObj.update_sent()
        subObj.update_sent()
    sleep(30)
    #Send follow ups
    for text in texts:
        errCode = text["Message"][0]
        asObj = text["Number"]
        
        if msgObj.follow_up in ('', None):
            text.update({"Followup":(-2, "No follow up.")})
        elif errCode == 0:
            #Only send the follow up if the the message was sucessful
            f_res = asObj.send_follow_up(msgObj)
            text.update(f_res)
        else:
            text.update({"Followup":(4, "Message failed, did not attempt.")})
        
    out = {"texts":texts, "msgObj":msgObj}
    email_send_results(out)
    return out
    
def email_send_results(staOutput):
    msgObj = staOutput["msgObj"]
    
    subject = msgObj.subscription.name + " sent!"
    from_email = get_value("from_email")
    to = get_value("to_emails")
    
    text_content = 'Send to all results:'
    html_content = render_to_string('send_results.html', staOutput)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()