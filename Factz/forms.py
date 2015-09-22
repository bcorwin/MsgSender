from django import forms
from Factz.models import Subscription

class uploadFactz(forms.Form):
    file = forms.FileField()
    subscription = forms.ModelChoiceField(queryset=Subscription.objects.all().order_by('name'))
    overwrite = forms.BooleanField(required=False)