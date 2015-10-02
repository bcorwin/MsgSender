import Factz.do as do
from Factz.models import Subscription, sentMessage, activeSubscription
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
from random import randint
from time import sleep

def dailysend2():

    now = timezone.now()
    today = now.replace(hour=0,minute=0,second=0,microsecond=0)

    #Fetch active subscriptions not sent today (UTC)
    active_subs = Subscription.objects.all().filter(active=True)
    active_subs = active_subs.filter(Q(last_sent__lt=today)|Q(last_sent=None))

    #Pick up any blank/old sends and set next_send
    update_subs = active_subs.filter(Q(next_send__lt=today)|Q(next_send=None))
    for S in update_subs:
        
        #First, quit if today is invalid for the subscription
        if not S.check_today(): break

        #Default start time/duration -> 16:00 - 23:45 UTC
        start_time = S.start_time()
        send_delay = S.wait_seconds()
        end_time = start_time + send_delay
        if end_time > 85500: end_time = 85500 #Never send after 23:45 UTC
        delay = randint(start_time,end_time) #Delay in seconds

        #Transform the delay from seconds to minutes, dropping the remainder
        hours = delay//3600
        remainder = delay%3600
        minutes = remainder//60
        next_send = datetime(now.year,now.month,now.day,hours,minutes)
        S.next_send = timezone.make_aware(next_send)
        S.save()

    #Filter to records where next_send is today and is in the past
    send_subs = active_subs.filter(next_send__gte=today)
    send_subs = send_subs.filter(next_send__lt=now)
    for S in send_subs:
        
        #Record start timse for the subscription run
        sm = sentMessage(subscription=S)
        sm.scheduled_start = S.next_send
        sm.actual_start = timezone.now() #Don't use just 'now'; it'll be stale

        #Perform the sends and clear next_send
        res = do.send_to_all(S)
        S.next_send = None
        S.last_sent = now
        S.save()

        #Record the end time, run time, and message for the subscription run
        sm.message = res["msgObj"]
        sm.actual_end = timezone.now() #Don't use just 'now'; it'll be stale
        sm.calc_runtime()
        sm.save()
        
        #Set result metrics for the subscription run; refactor this block
        sm.msg_success = res['msg_status']['succ']
        sm.msg_fail = res['msg_status']['fail']
        sm.msg_na = res['msg_status']['na']
        sm.fu_success = res['fu_status']['succ']
        sm.fu_fail = res['fu_status']['fail']
        sm.fu_na = res['fu_status']['na']
        sm.save()        

    #Loop over new users without any sends
    new_users = activeSubscription.objects.all()
    new_users = new_users.filter(active=True,last_sent=None,inserted_date__gte=today-timedelta(days=1))
    for U in new_users:
        #Quit if the subscription is inactive or doesn't have a past send logged
        subs = U.subscription
        if (subs.active == False or subs.last_sent is None): continue
        
        #Find the most recent sentMessage or quit if none exist
        sentM = sentMessage.objects.all().filter(subscription=subs)
        sentM = sentM.order_by('-scheduled_start')
        try: sm = sentM[0]
        except: continue
        msgObj = sm.message
        
        #Immediately send the message; don't update subscription/message counters
        #Eventually this code needs to be merged into a unified functions with do.send_to_all
        res = U.send_message(msgObj)        
        sleep(15)
        if msgObj.follow_up in ('', None) and res['Message'][0] == 0:
            U.send_follow_up(msgObj)       
        #Results not currently being updated on sm record

    return(None)



def dailysend():
    
    now = timezone.now()
    today = now.replace(hour=0,minute=0,second=0,microsecond=0)
    
    #Fetch subscriptions (active, not sent today, not scheduled today)
    subs = Subscription.objects.filter(active=True)
    subs = subs.filter(Q(last_sent__lt=today)|Q(last_sent=None))
    subs = subs.filter(Q(next_send__lt=today)|Q(next_send=None))
    
    for S in subs:
        
        #First, quit if today is invalid for the subscription
        if not S.check_today(): break

        #Default start time/duration -> 16:00 - 23:45 UTC
        start_time = S.start_time()
        end_time = S.end_time()
        if end_time > 85500: end_time = 85500 #Never send after 23:45 UTC
        delay = randint(start_time,end_time) #Delay in seconds

        #Transform the delay from seconds to minutes, dropping the remainder
        hours = delay//3600
        remainder = delay%3600
        minutes = remainder//60
        next_send = datetime(now.year,now.month,now.day,hours,minutes)
        S.next_send = timezone.make_aware(next_send)
        S.save()
        
        #Create a corresponding sentMessage record
        sm = sentMessage(subscription=S)
        sm.scheduled_start = S.next_send
        sm.run_date = today
        sm.message = do.next_message(S)
        sm.save()
        
    #Fetch activeSubscriptions (active, not sent today, not scheduled today)
    actSubs = activeSubscription.objects.filter(active=True)
    actSubs = actSubs.filter(Q(last_sent__lt=today)|Q(last_sent=None))
    actSubs = actSubs.filter(Q(next_send__lt=today)|Q(next_send=None))

    #Find related sentMessage for today and set next_send
    for A in actSubs:
        sm = getSM(S,today)
        if sm is not None:
            A.next_send = next_send
            A.save()
    
    #Fetch activeSubscriptions (active, never sent before, overdue to send)
    lateSends = activeSubscription.objects.filter(active=True)
    lateSends = lateSends.filter(last_sent=None)
    lateSends = lateSends.filter(next_send__lt=now)
    
    res = None
    
    for L in lateSends:
        sm = getSM(L.subscription.today)        
        msg = sm.message
        res = send_to_actSub(L, msg, sm, res)
    
    #Fetch activeSubscriptions (active, next_send today but in the past)
    currentSends = activeSubscription.objects.filter(active=True)
    currentSends = currentSends.filter(next_send__gte=today)
    currentSends = currentSends.filter(next_send__lt=now)
    
    #Creating a unique list of sentMessages
    currentSM = set()
    for C in currentSends:
        sm = getSM(C.subscription,today)
        currentSM.add(sm)
    
    res = None    
    
    for sm in currentSM:

        sm.actual_start = timezone.now() #Don't use just 'now'; it'll be stale
        
        msg = sm.message
        filteredSends = currentSends.filter(subscription=sm.subscription)           

        for F in filteredSends:            
            res = send_to_actSub(F, msg, sm, res)
            F.update_sent(msg)
    
        sm.actual_end = timezone.now() #Don't use just 'now'; it'll be stale
        sm.calc_runtime()
        sm.save()
        
        sm.subscription.update_sent()
        msg.update_sent()        
        
        #Send summary email
    
    return(None)

#Issues: doesn't gracefully handle missing records or multiple returns
def getSM(subscription, run_date):
    try:
        sm = sentMessage.get(subscription=subscription,run_date=run_date)
    except:
        sm = None
    return sm
    
def send_to_actSub(actSub, msg, sm, res):
    
    #do message send (update_sent already handled)
    #do fu send (update_sent already handled)
    
    actSub.msg_success += 0
    actSub.msg_fail += 0
    actSub.msg_na += 0
    actSub.fu_success += 0
    actSub.fu_fail += 0
    actSub.fu_na += 0
    actSub.save()
    
    sm.msg_success += 0
    sm.msg_fail += 0
    sm.msg_na += 0
    sm.fu_success += 0
    sm.fu_fail += 0
    sm.fu_na += 0
    sm.save()
    
    return res