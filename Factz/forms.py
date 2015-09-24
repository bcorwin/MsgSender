from django import forms
from Factz.models import Subscription, Message

class uploadFactz(forms.Form):
    file = forms.FileField()
    subscription = forms.ModelChoiceField(queryset=Subscription.objects.all().order_by('name'))
    overwrite = forms.BooleanField(required=False)
    
class sendForm(forms.Form):
    subscription = forms.ModelChoiceField(queryset=Subscription.objects.all().order_by('name'))
    message = forms.ModelChoiceField(queryset=Message.objects.all().order_by('subscription'), required=False, empty_label="*Randomly select message*")