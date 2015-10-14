from Factz.models import sentMessage
from Factz.do import email_send_results
from django.utils import timezone
from datetime import timedelta

def dailyemail():
    prev_day = timezone.now().date() - timedelta(days=1)
    
    sMobjs = sentMessage.objects.filter(next_send_date=prev_day)
    msgObjs = list(set([sM.message for sM in sMobjs]))
    
    for msgObj in msgObjs:
        sMobjs_subset = sMobjs.filter(message=msgObj)
        texts = [{"Number":sM.active_subscription, "Message":(sM.message_code, sM.message_status), "Followup": (sM.followup_code, sM.followup_status)} for sM in sMobjs_subset]
        output = {"texts":texts, "msgObj":msgObj}
        email_send_results(output)