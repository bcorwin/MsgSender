import Factz.do as do
from Factz.models import Subscription, sentMessage, activeSubscription, dailySend
from django.utils import timezone
from datetime import datetime
from random import randint

def dailysend():

    now = timezone.now()
    #today = now.replace(hour=0,minute=0,second=0,microsecond=0)
    today = now.date()

<<<<<<< HEAD
    #Fetch subscriptions (active, not sent today, not scheduled today)
    subs = Subscription.objects.filter(active=True)
    subs = subs.filter(Q(last_sent__lt=today)|Q(last_sent=None))
    subs = subs.filter(Q(next_send__lt=today)|Q(next_send=None))

=======
    #Fetch active subscriptions and loop
    subs = Subscription.objects.filter(active=True)
>>>>>>> refs/remotes/bcorwin/master
    for S in subs:

        #First, quit if today is invalid for the subscription
        if not S.check_today(): continue

<<<<<<< HEAD
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
=======
        #Second, look for a dailySend record for today
        dS = None
        [dS,new] = dailySend.objects.get_or_create(subscription=S,next_send_date=today)

        #Create a new dailySend record if one doesn't exist
        if new:
            msg = do.next_message(S)
            dS.message = msg
            dS.save()
            set_send_time(S,dS)

            #If the dailySend is new, create sentMessages for all activeSubscriptions
            activeSubs = activeSubscription.objects.filter(subscription=S,active=True)
            for aS in activeSubs:
                [sM,new] = sentMessage.objects.get_or_create(active_subscription=aS,message=msg,next_send_date=today,daily_send=dS)
                if new:
                    sM.attempted = False
                    sM.next_send = get_send_time(dS,aS)
                    sM.save()

    #Now try to send any eligible sentMessage records
    sentMessages = []
    toSend = sentMessage.objects.filter(next_send_date=today,next_send__lt=now)
    for sM in toSend:
        if sM.sent_time is not None: continue
        if sM.active_subscription.active == False: continue
        if sM.active_subscription.subscription.active == False: continue
        sentMessages.append(sM)
        sM.attempted = True
        sM.save()
    if sentMessages != []: do.send_to_all(sentMessages)

    return(None)

def set_send_time(S, dailySend):

    now = timezone.now()

    start_time = S.start_time()
    end_time = S.end_time()
    if end_time > 85500: end_time = 85500 #Never send after 23:45 UTC
    delay = randint(start_time,end_time) #Delay in seconds

    #Transform the delay from seconds to minutes, dropping the remainder
    hours = delay//3600
    remainder = delay%3600
    minutes = remainder//60
    send_time = datetime(now.year,now.month,now.day,hours,minutes)
    send_time = timezone.make_aware(send_time)

    S.next_send = send_time
    dailySend.next_send = send_time

    S.save()
    dailySend.save()

    return(send_time)

def get_send_time(dailySend, activeSubscription):

    send_time = dailySend.next_send

    return(send_time)
>>>>>>> refs/remotes/bcorwin/master
