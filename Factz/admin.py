from django.contrib import admin
from Factz.models import Variable, Message, Subscription, Number, activeSubscription

def set_active(modeladmin, request, queryset):
    queryset.update(active=True)

def set_inactive(modeladmin, request, queryset):
    queryset.update(active=False)

class activeSubAdmin(admin.ModelAdmin):
    list_display = ['number', 'subscription', 'active']
    actions = [set_active, set_inactive]
    
class messageAdmin(admin.ModelAdmin):    
    list_display = ['subscription', 'message', 'follow_up', 'last_sent', 'active']
    actions = [set_active, set_inactive]
    
class numberAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'last_sent']

class subAdmin(admin.ModelAdmin):
    list_display = ['name', 'last_sent']
    
class varAdmin(admin.ModelAdmin):
    list_display = ['name', 'val']

admin.site.register(Message, messageAdmin)
admin.site.register(Number, numberAdmin)
admin.site.register(Subscription, subAdmin)
admin.site.register(Variable, varAdmin)
admin.site.register(activeSubscription, activeSubAdmin)