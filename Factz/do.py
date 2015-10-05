#Use do to store functions that may depend on models
from Factz.models import Number, Variable, Message, activeSubscription, Subscription, Rating
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime
from random import random
from time import sleep
import csv

def get_value(varname):
    '''
    Grab the val for varname from the Variable table
    '''
    try:
        val = Variable.objects.get(name=varname).val
    except:
        val = None
    return val
    
def weighted_choice(obj, weights):
    if len(obj) != len(weights):
        raise ValidationError
    totals = []
    running_total = 0

    for w in weights:
        running_total += w
        totals.append(running_total)

    rnd = random() * running_total
    for i, total in enumerate(totals):
        if rnd < total:
            return obj[i]
    
def next_message(subObj):
    '''
    Randomly select the next message. Older messages have higher weight.
    Weight =  number of days it's been since it was last sent
    '''
    today = datetime.utcnow().date()
    msg_set = Message.objects.all().filter(subscription=subObj, active=True)
    if msg_set.exists() == False: return None

    min_date = [m.last_sent.date() for m in msg_set if m.last_sent != None]
    min_date = min(min_date) if len(min_date) >0 else today
    
    ages = [m.last_sent.date() if m.last_sent != None else min_date for m in msg_set]
    ages = [int(1.25**((today - ls).days + 1)) for ls in ages]

    #randomly select a message given the above weights
    res = weighted_choice(msg_set, ages)
    return res

def number_exist(phone_number):
    '''
    If a number is in the database, return it otherwise return None
    '''
    num = Number.objects.filter(phone_number=phone_number)
    if num.exists():
        return num.get()
    else:
        return None

def sub_exist(name):
    '''
    If a subscription is in the database, return it otherwise return None
    '''
    sub = Subscription.objects.filter(name__iexact=name)
    if sub.exists():
        return sub.get()
    else:
        return None

def add_number(num):
    '''
    Adds a number to the database and returns it
    If the number is already in the database the function returns it
    '''
    numObj = Number.objects.filter(phone_number=num)
    if numObj.exists():
        num = numObj.get()
    else:
        num = Number(phone_number=num)
        num.save()
    return num
    
def add_rating(numObj, msgObj, rating):
    '''
    Adds a rating (and validates it)
    '''
    R = Rating(number=numObj, message=msgObj, rating=rating)
    try:
        R.full_clean()
        R.save()
        return None
    except ValidationError as e:
        return e

def upload_file(f, sub, overwrite):
    '''
    Reads a csv file (Format: ID, Message, Follow_up, Source) and adds to db.
    '''
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

def send_to_all(smObjs):
    '''
    smObjs should be a list of sentMessage objects
    '''
    texts = []
    msg_status = {'succ':0,'fail':0,'na':0}
    fu_status =  {'succ':0,'fail':0,'na':0}
    
    for smObj in smObjs:
        user = smObj.active_subscription
        add = {"Number":user}
        #To do: deal with when message is null and we want to send a custom message instead.
        msgObj = smObj.message
        res = user.send_message(msgObj)
        msg_status = update_status(msg_status, res, 'Message')
        add.update(res)
        texts.append(add)
        
    #To do: This needs to be moved, but to where?
    #msgObj.update_sent()
    #subObj.update_sent()
        
    sleep(30)
    
    for text in texts:
        errCode = text["Message"][0]
        asObj = text["Number"]
        if msgObj.follow_up in ('', None):
            f_res = {"Followup":(-2, "No follow up.")}
            text.update(f_res)
        elif errCode == 0:
            #Only send the follow up if the the message was successful
            f_res = asObj.send_follow_up(msgObj)
            text.update(f_res)
        else:
            f_res = {"Followup":(4, "Message failed, did not attempt.")}
            text.update(f_res)
        fu_status = update_status(fu_status, f_res, 'Followup')

    out = {"texts":texts, "msgObj":msgObj, "msg_status":msg_status, "fu_status":fu_status}
    email_send_results(out)

    return out

def update_status(counter, result, msg_type):
    if result[msg_type][0] == 0:
        counter['succ'] += 1
    elif result[msg_type][0] > 0:
        counter['fail'] += 1
    elif result[msg_type][0] < 0:
        counter['na'] += 1
    return counter

def email_send_results(staOutput):
    '''
    Emails the output of send_to_all using the send_results.html template
    '''
    msgObj = staOutput["msgObj"]

    subject = msgObj.subscription.name + " sent!"
    from_email = get_value("from_email")
    to = get_value("to_emails")
    if to == None:
        return None

    text_content = 'Send to all results:'
    html_content = render_to_string('send_results.html', staOutput)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return None
