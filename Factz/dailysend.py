import Factz.do as do
from Factz.models import Subscription, sentMessage, activeSubscription
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
from random import randint
from time import sleep

def dailysend():

    now = timezone.now()
    today = now.replace(hour=0,minute=0,second=0,microsecond=0)

    #Fetch subscriptions (active, not sent today, not scheduled today)
    subs = Subscription.objects.filter(active=True)
    subs = subs.filter(Q(last_sent__lt=today)|Q(last_sent=None))
    subs = subs.filter(Q(next_send__lt=today)|Q(next_send=None))

    for S in subs:

        #First, quit if today is invalid for the subscription
        if not S.check_today(): continue

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

        #Create a corresponding sentMessage record or update an existing one
        sm = getSM(S, today)
        if sm is None:
            sm = sentMessage(subscription=S)
            sm.run_date = today
        sm.scheduled_start = S.next_send
        sm.message = do.next_message(S)
        sm.save()

    #Fetch activeSubscriptions (active, not sent today, not scheduled today)
    actSubs = activeSubscription.objects.filter(active=True)
    actSubs = actSubs.filter(Q(last_sent__lt=today)|Q(last_sent=None))
    actSubs = actSubs.filter(Q(next_send__lt=today)|Q(next_send=None))

    #Find related sentMessage for today and set next_send
    for A in actSubs:
        sm = getSM(A.subscription,today)
        if sm is not None:
            A.next_send = sm.scheduled_start
            A.save()

    #Fetch activeSubscriptions (active, never sent before, overdue to send)
    lateSends = activeSubscription.objects.filter(active=True)
    lateSends = lateSends.filter(last_sent=None)
    lateSends = lateSends.filter(next_send__lt=now)

    res = None
    for L in lateSends:
        sm = getSM(L.subscription,today)
        msg = sm.message
        res = send_to_actSub(L, msg, sm, res)
        L.update_sent(msg)

    #Fetch activeSubscriptions (active, next_send today but in the past)
    currentSends = activeSubscription.objects.filter(active=True)
    currentSends = actSubs.filter(last_sent__lt=today)
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

def getSM(subscription, run_date):
    sm = sentMessage.objects.filter(subscription=subscription,run_date=run_date)
    if sm.exists():
        sm = sm[0]
    else:
        sm = None
    return sm

def send_to_actSub(actSub, msg, sm, res):

    #do message send (update_sent already handled)
    #do fu send (update_sent already handled)
    '''
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
    '''
    return res
