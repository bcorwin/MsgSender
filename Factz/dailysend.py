import Factz.do as do
from Factz.models import Subscription
from django.db.models import Q
from django.utils import timezone
from random import randint

def dailysend():

    now = timezone.now()

    #Fetch active subscriptions not sent today (UTC)
    active_subs = Subscription.objects.all().filter(active=True)
    active_subs = active_subs.filter(Q(last_sent__lt=now.date())|Q(last_sent=None))

    #Pick up any blank/old sends and set next_send
    update_subs = active_subs.filter(Q(next_send__lt=now.date())|Q(next_send=None))
    for S in update_subs:
        #First, quit if today is invalid for the subscription
        if not S.check_today(): break

        #Default start time/duration -> 16:00 - 23:45 UTC
        start_time = S.start_time()
        send_delay = S.wait_seconds()
        end_time = start_time + send_delay
        if end_time > 85500: end_time = 85500 #Never send after 23:45 UTC
        delay = randint(start_time,end_time) #Delay in seconds
        
        hours = delay//3600
        remainder = delay%3600
        minutes = remainder//60
        S.next_send = datetime(now.year,now.month,now.day,hours,minutes)
        S.save()
    
    #Filter to records where next_send is today and is in the past
    send_subs = active_subs.filter(next_send__gte=now.date())
    send_subs = send_subs.filter(next_send__lt=now)
    for S in send_subs:
        #do.send_to_all(S) #Keep those commented until the scheduler works
        S.next_send = None
        S.save()

    return(None)
