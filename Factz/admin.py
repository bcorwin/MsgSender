from django.contrib import admin
from Factz.models import Variable, Message, Subscription, Number, activeSubscription, sentMessage, Rating

def set_active(modeladmin, request, queryset):
    queryset.update(active=True)

def set_inactive(modeladmin, request, queryset):
    queryset.update(active=False)

class activeSubAdmin(admin.ModelAdmin):
    list_display = ['number', 'subscription', 'last_sent', 'active']
    list_filter = ['subscription', 'active', 'last_sent']
    actions = [set_active, set_inactive]
    
class messageAdmin(admin.ModelAdmin):    
    list_display = ['subscription', 'message', 'follow_up', 'last_sent', 'get_rating', 'active']
    list_filter = ['subscription', 'active', 'last_sent']
    actions = [set_active, set_inactive]
    
class numberAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'phone_number', 'last_sent']

class subAdmin(admin.ModelAdmin):
    list_display = ['name', 'last_sent', 'next_send', 'active']
    list_filter = ['active', 'last_sent', 'next_send']
    
class varAdmin(admin.ModelAdmin):
    list_display = ['name', 'val']
    
class smAdmin(admin.ModelAdmin):
    list_display = ['scheduled_start', 'actual_start', 'actual_end', 'actual_run', 'message', 'subscription']
    list_filter = ['subscription', 'scheduled_start', 'actual_run']

class ratingAdmin(admin.ModelAdmin):
    list_display = ['number', 'message', 'rating']
    list_filter = ['number', 'rating']
    
admin.site.register(Message, messageAdmin)
admin.site.register(Number, numberAdmin)
admin.site.register(Subscription, subAdmin)
admin.site.register(Variable, varAdmin)
admin.site.register(activeSubscription, activeSubAdmin)
admin.site.register(sentMessage, smAdmin)
admin.site.register(Rating, ratingAdmin)
