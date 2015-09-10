from django.contrib import admin
from Factz.models import Variable, Message, Subscription, Number

admin.site.register(Message)
admin.site.register(Number)
admin.site.register(Subscription)
admin.site.register(Variable)