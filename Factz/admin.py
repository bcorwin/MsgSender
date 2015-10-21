from django.contrib import admin, messages
from Factz.models import Variable, Message, Subscription, Number, activeSubscription, sentMessage, dailySend, customMessage
from Factz.do import add_custom_messages
from django.utils import timezone

def send_now(modeladmin, request, queryset):
    toSend = [sM for sM in queryset if sM.sent_time in (None, '') ]
    if len(toSend) != len(queryset): messages.info(request, "Can only send now if message has not been sent yet.")
    if len(toSend) == 0: messages.error(request, "No message next send times were changed.")
    for sM in toSend:
        sM.next_send = timezone.now()
        sM.save()

def select_custom(modeladmin, request, queryset):
    num = len(queryset)
    if num == 0: pass
    elif num > 1: messages.error(request, "Please select only one custom message.")
    else:
        cM = queryset[0]
        cM.selected = True
        cM.save()

def send_custom_message(modeladmin, request, queryset):
    add_custom_messages(queryset)
    
def set_active(modeladmin, request, queryset):
    queryset.update(active=True)

def set_inactive(modeladmin, request, queryset):
    queryset.update(active=False)

class sentMsgInline(admin.TabularInline):
    model = sentMessage
    fields = ['next_send', 'sent_time', 'print_msg', 'rating', 'attempted']
    readonly_fields = ['next_send', 'sent_time', 'print_msg', 'rating', 'attempted']
    show_change_link = True
    extra = 0
    
class activeSubInline(admin.TabularInline):
    model = activeSubscription
    fields = ['subscription', 'message', 'last_sent', 'active']
    readonly_fields = ['subscription', 'message', 'last_sent']
    show_change_link = True
    extra = 0

class activeSubAdmin(admin.ModelAdmin):
    list_display = ['number', 'subscription', 'last_sent', 'active']
    list_filter = ['subscription', 'active', 'last_sent']
    inlines = [sentMsgInline]
    actions = [set_active, set_inactive, send_custom_message]
    
class messageAdmin(admin.ModelAdmin):    
    list_display = ['subscription', 'message', 'follow_up', 'last_sent', 'get_rating', 'active']
    list_filter = ['subscription', 'active', 'last_sent']
    search_fields = ['message','follow_up']
    actions = [set_active, set_inactive]
    
class numberAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'phone_number', 'last_sent']
    actions = [send_custom_message]
    inlines = [activeSubInline]

class subAdmin(admin.ModelAdmin):
    list_display = ['name', 'next_send', 'active']
    list_filter = ['active', 'next_send']
    actions = [send_custom_message]
    
class varAdmin(admin.ModelAdmin):
    list_display = ['name', 'val']
    
class dsAdmin(admin.ModelAdmin):
    list_display = ['subscription', 'next_send_date', 'message']
    list_filter = ['subscription', 'next_send_date']
    inlines = [sentMsgInline]
    ordering = ['-next_send_date']
    
class smAdmin(admin.ModelAdmin):
    list_display = ['active_subscription', 'next_send', 'sent_time', 'print_msg', 'rating', 'attempted']
    list_filter = ['next_send_date', 'sent_time', 'rating', 'attempted', 'is_custom']
    readonly_fields = ['next_send_date', 'is_custom']
    actions = [send_now]
    
class cmAdmin(admin.ModelAdmin):
    list_display = ['message', 'last_sent', 'selected']
    list_filter = ['last_sent', 'selected']
    search_fields = ['message']
    readonly_fields = ['last_sent']
    actions = [select_custom]
    
admin.site.register(Message, messageAdmin)
admin.site.register(Number, numberAdmin)
admin.site.register(Subscription, subAdmin)
admin.site.register(Variable, varAdmin)
admin.site.register(activeSubscription, activeSubAdmin)
admin.site.register(sentMessage, smAdmin)
admin.site.register(dailySend, dsAdmin)
admin.site.register(customMessage, cmAdmin)
