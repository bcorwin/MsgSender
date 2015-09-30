import Factz.do as do
from Factz.models import Subscription, sentMessage, activeSubscription
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from random import randint
from time import sleep

def dailysend():

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
    new_users = activeSubscription.objects.all().filter(active=True,last_sent=None)
    for U in new_users:
        
        #Quit if the subscription is inactive or doesn't have a past send logged
        subs = U.subscription
        if subs.active == False or subs.last_sent is None: break
            
        #Find the most recent sentMessage or quit if none exist
        sentM = sentMessage.objects.all().filter(subscription=subs)
        sentM = sentM.order_by('-scheduled_start')
        try: sm = sentM[0]
        except: break
        msgObj = sm.message
        
        #Immediately send the message; don't update subscription/message counters
        #Eventually this code needs to be merged into a unified functions with do.send_to_all
        res = U.send_message(msgObj)        
        sleep(30)
        if msgObj.follow_up in ('', None) and res['Message'][0] == 0:
            U.send_follow_up(msgObj)       

    return(None)
