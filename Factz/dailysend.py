import Factz.do as do
import Factz.messaging as messaging
from Factz.models import Subscription, activeSubscription
from datetime import datetime
    
def dailysend():
    
    subs = Subscription.objects.all().filter(active=True)
    subs = subs.filter(last_sent__lt=datetime.now().date())
    #determine send time and wait
    
    for S in subs:
        
        msg = None          
        msg = do.next_message(S)
        
        act_subs = None
        act_subs = activeSubscription.objects.all().filter(subscription_id=S).filter(active=True)

        for A in act_subs:
            
            num = None            
            num = A.number_id
            
            val = None
            val = messaging.send_message(msg,num)
            
            if val[0] == 1:
                A.message_id = msg
                A.message_cnt += 1
                A.last_sent = datetime.now()
                num.last_sent = datetime.now()
    
    return()