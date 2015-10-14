import Factz.do as do
from Factz.models import Subscription, sentMessage, activeSubscription, dailySend
from django.utils import timezone
from datetime import datetime
from random import randint

def dailysend():

    now = timezone.now()
    #today = now.replace(hour=0,minute=0,second=0,microsecond=0)
    today = now.date()

    #Fetch active subscriptions and loop
    subs = Subscription.objects.filter(active=True)
    for S in subs:

        #First, quit if today is invalid for the subscription
        if not S.check_today(): continue

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
                    sM.attempted = 0
                    sM.next_send = get_send_time(dS,aS)
                    sM.save()

    #Now try to send any eligible sentMessage records
    sentMessages = []
    toSend = sentMessage.objects.filter(next_send_date=today,next_send__lt=now,attempted__lt=2)
    for sM in toSend:
        if sM.sent_time is not None: continue
        if sM.active_subscription.active == False: continue
        if sM.active_subscription.subscription.active == False: continue
        sentMessages.append(sM)
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
