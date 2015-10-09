import Factz.do as do
from Factz.models import Subscription, sentMessage, activeSubscription, dailySend
from django.utils import timezone
from datetime import datetime
from random import randint

def new_send_time(S, activeSubscription):
    
    now = timezone.now()
    
    #Default start time/duration -> 16:00 - 23:45 UTC
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
    
    return(send_time)

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

            #If the dailySend is new, create sentMessages for all activeSubscriptions
            activeSubs = activeSubscription.objects.filter(subscription=S,active=True)
            for aS in activeSubs:
                [sM,new] = sentMessage.objects.get_or_create(active_subscription=aS,message=msg,next_send_date=today)
                if new:
                    sM.attempted = False
                    sM.next_send = new_send_time(S,aS)
                    sM.save()

    #Now try to send any eligible sentMessage records
    toSend = sentMessage.objects.filter(next_send_date__gte=today,next_send__lt=now)
    for dS in toSend:
        if toSend.last_sent is not None: continue
        if toSend.active_subscription.active == False: continue
        if toSend.active_subscription.subscription.active == False: continue
        do.send_to_all(dS)
        dS.attempted = True
        dS.save()        

    return(None)
    