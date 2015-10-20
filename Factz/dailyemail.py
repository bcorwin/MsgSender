from Factz.models import sentMessage, Number
from Factz.do import email_send_results, email_new_users
from django.utils import timezone
from datetime import timedelta

def dailyemail():
    prev_day = timezone.now().date() - timedelta(days=1)
    
    sMobjs = sentMessage.objects.filter(next_send_date=prev_day)

    #Messages    
    msgObjs = list(set([sM.message for sM in sMobjs if sM.message is not None]))
    
    for msgObj in msgObjs:
        sMobjs_subset = sMobjs.filter(message=msgObj)
        texts = [{"Number":sM.active_subscription,
                  "Message":(sM.message_code, sM.message_status),
                  "Followup": (sM.followup_code, sM.followup_status),
                  "Rating": sM.rating if sM.rating is not None else ''}
                      for sM in sMobjs_subset]
        output = {"texts":texts, "msgObj":msgObj, "custom": False}
        email_send_results(output)
        
    #Custom messages
    cmsgObjs = list(set([sM.custom_message for sM in sMobjs if sM.custom_message is not None]))
    
    for cmsgObj in cmsgObjs:
        sMobjs_subset = sMobjs.filter(custom_message=cmsgObj)
        texts = [{"Number":sM.active_subscription,
                  "Message":(sM.message_code, sM.message_status)}
                      for sM in sMobjs_subset]
        output = {"texts":texts, "msgObj":cmsgObj, "custom": True}
        email_send_results(output)
        
    #New users
    new_users = Number.objects.filter(inserted_date__gte=prev_day)
    if len(new_users) > 0: email_new_users(new_users)