from django.contrib import admin
from Factz.models import Variable, Message, Subscription, Number, activeSubscription, sentMessage, dailySend

def set_active(modeladmin, request, queryset):
    queryset.update(active=True)

def set_inactive(modeladmin, request, queryset):
    queryset.update(active=False)

class sentMsgInline(admin.TabularInline):
    model = sentMessage
    fields = ['next_send', 'sent_time', 'message', 'rating', 'attempted']
    readonly_fields = ['next_send', 'sent_time', 'message', 'rating', 'attempted']
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
    actions = [set_active, set_inactive]
    
class messageAdmin(admin.ModelAdmin):    
    list_display = ['subscription', 'message', 'follow_up', 'last_sent', 'get_rating', 'active']
    list_filter = ['subscription', 'active', 'last_sent']
    search_fields = ['message','follow_up']
    actions = [set_active, set_inactive]
    
class numberAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'phone_number', 'last_sent']
    inlines = [activeSubInline]

class subAdmin(admin.ModelAdmin):
    list_display = ['name', 'last_sent', 'next_send', 'active']
    list_filter = ['active', 'last_sent', 'next_send']
    
class varAdmin(admin.ModelAdmin):
    list_display = ['name', 'val']
    
class dsAdmin(admin.ModelAdmin):
    list_display = ['subscription', 'next_send_date', 'message']
    list_filter = ['subscription', 'next_send_date']
    inlines = [sentMsgInline]
    ordering = ['-next_send_date']
    
class smAdmin(admin.ModelAdmin):
    list_display = ['active_subscription', 'next_send', 'sent_time', 'message', 'rating', 'attempted']
    list_filter = ['next_send_date', 'sent_time', 'rating', 'attempted']
    
admin.site.register(Message, messageAdmin)
admin.site.register(Number, numberAdmin)
admin.site.register(Subscription, subAdmin)
admin.site.register(Variable, varAdmin)
admin.site.register(activeSubscription, activeSubAdmin)
admin.site.register(sentMessage, smAdmin)
admin.site.register(dailySend, dsAdmin)
