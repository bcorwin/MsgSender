from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from Factz.utils import rand_code, format_number
from Factz.messaging import send_test_message, send_message
from django.utils import timezone
from datetime import datetime
from math import ceil

class Variable(models.Model):
    name = models.CharField(max_length=64, unique=True)
    val = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name + "=" + self.val    
    
class Subscription(models.Model):
    name = models.CharField(max_length=16, unique=True)
    active = models.BooleanField(default=True)
    last_sent = models.DateTimeField(null=True, blank=True)
    next_send = models.DateTimeField(null=True, blank=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    #Revamp: add end_time and auto-caluclate send_delay
    send_base = models.TimeField(default=datetime(1,1,1,16))
    send_delay = models.PositiveIntegerField(default=465)

    #Could we use a text field with validation instead?
    send_monday = models.BooleanField(default=True)
    send_tuesday = models.BooleanField(default=True)
    send_wednesday = models.BooleanField(default=True)
    send_thursday = models.BooleanField(default=True)
    send_friday = models.BooleanField(default=True)
    send_saturday = models.BooleanField(default=True)
    send_sunday = models.BooleanField(default=True)
    
    def get_last_message(self):
        out = dailySend.objects.all().filter(subscription=self).order_by("-next_send_date")
        out = out[0].message if out.exists() else None
        return(out)
    
    def wait_seconds(self):
        val = self.send_delay*60
        return(val)
    
    def start_time(self):
        hours = self.send_base.hour
        minutes = self.send_base.minute
        val = (hours*60+minutes)*60
        return(val)
    
    def check_today(self):
        today = datetime.today().weekday()
        if today == 0:
            val = self.send_monday
        elif today == 1:
            val = self.send_tuesday
        elif today == 2:
            val = self.send_wednesday
        elif today == 3:
            val = self.send_thursday
        elif today == 4:
            val = self.send_friday
        elif today == 5:
            val = self.send_saturday
        elif today == 6:
            val = self.send_sunday
        return(val)

    def update_sent(self):
        self.last_sent = timezone.now()
        self.save()
        
    def __str__(self):
        return self.name

class Message(models.Model):
    sheet_id = models.IntegerField()
    message = models.CharField(max_length=320)
    follow_up = models.CharField(max_length=160)
    source = models.CharField(max_length=160)
    subscription = models.ForeignKey(Subscription, on_delete=models.PROTECT)
    active = models.BooleanField(default=True)
    last_sent = models.DateTimeField(null=True, blank=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def get_rating(self):
        ratings = [r.rating for r in Rating.objects.filter(message=self)]
        if len(ratings) > 0:
            return round(sum(ratings)/len(ratings), 1)
        else:
            return None
    get_rating.short_description = "Rating"
    
    def update_sent(self):
        self.last_sent = timezone.now()
        self.save()
    
    def __str__(self):
        if len(self.message) > 160:
            out = self.message[0:159]
            out += "..."
        else:
            out = self.message
        return out
        
    class Meta:
        unique_together = ('sheet_id', 'subscription')
        
class Number(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    confirmation_code = models.CharField(max_length=6, default=rand_code)
    confirmed = models.BooleanField(default=False)
    last_sent = models.DateTimeField(null=True, blank=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    #Optional information
    name = models.CharField(max_length=32, blank=True, null=True)
    email = models.CharField(max_length=32, blank=True, null=True)
    
    def toggle_active(self, subObj, status=None):
        '''
        Either set the active status of a number/subscription pair to status
        or toggle the current status.
        If it does not exist, create it first then activate it.
        Returns the activeSubscription object (asObj)
        '''
        asObj = self.get_active_subscription(subObj)
        if not asObj.exists():
            asObj = activeSubscription(number=self, subscription=subObj)
            asObj.active = True
        else:
            asObj = asObj.get()
        asObj.active = status if status != None else not asObj.active
        asObj.save()
        return asObj
    
    def get_active_subscription(self, subObj):
        return activeSubscription.objects.filter(number=self, subscription=subObj)
    
    def get_last_message(self, subObj = None):
        '''
        Get the most recent message for a given subscription OR the most recent if subObj is None
        '''
        if subObj != None:
            asObj = activeSubscription.objects.filter(number=self, subscription=subObj)
        else:
            asObj = activeSubscription.objects.filter(number=self).order_by('-last_sent')
        
        if asObj.exists():
            asObj = asObj[0]
            out = asObj.message
        else:
            out = None
            
        return out
    
    def update_sent(self):
        self.last_sent = timezone.now()
        self.save()
    
    def save(self, *args, **kwargs):
        self.phone_number = format_number(self.phone_number)
        if not self.pk:
            chk = send_test_message(self)
            if chk[0] != 0:
                raise ValueError(chk[1])
            
        super(Number, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.name if self.name != None else self.phone_number
        
class activeSubscription(models.Model):
    number = models.ForeignKey(Number, on_delete=models.PROTECT)
    subscription = models.ForeignKey(Subscription, on_delete=models.PROTECT)
    message = models.ForeignKey(Message, blank=True, null=True, default=None, on_delete=models.PROTECT)
    active = models.BooleanField(default=True)
    last_sent = models.DateTimeField(null=True, blank=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def update_sent(self, msgObj):
        self.message = msgObj
        self.last_sent = timezone.now()
        self.number.update_sent()
        self.save()
    
    def send_message(self, msgObj):
        if self.active == True:
            res = send_message(msgObj, self)
            if res[0] == 0:
                self.update_sent(msgObj)
        else:
            res = (-1, "Not active.")
        return {"Message":res}
    
    def send_follow_up(self, msgObj):
        if self.active == True and msgObj.follow_up not in ('', None):
            res = send_message(msgObj, self, type="followup")
        elif self.active != True:
            res = (-1, "Not active.")
        else:
            res = (-2, "No follow up.")
        return {"Followup":res}
    
    def save(self, *args, **kwargs):
        is_new = True if not self.pk else False
        super(activeSubscription, self).save(*args, **kwargs)
        if is_new:
            msgObj = self.subscription.get_last_message()
            smObj = sentMessage(active_subscription=self, message=msgObj, next_send=timezone.now())
            smObj.save()
        
    def __str__(self):
        return str(self.number) + " " + str(self.subscription) + " (" + str(self.active) + ")"
        
    class Meta:
        unique_together = ('number', 'subscription')

class dailySend(models.Model):
    subscription = models.ForeignKey(Subscription)
    message = models.ForeignKey(Message)
    next_send_date = models.DateField()
    
class sentMessage(models.Model):
    active_subscription = models.ForeignKey(activeSubscription, null=True, blank=True, default=None, on_delete=models.PROTECT)
    message = models.ForeignKey(Message, null=True, blank=True, default=None, on_delete=models.PROTECT)
    next_send = models.DateTimeField()
    next_send_date = models.DateField()
    sent_time = models.DateTimeField(default=None, null=True, blank=True)
    attempted = models.BooleanField(default=False)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        self.next_send_date = self.next_send.date()
        super(sentMessage, self).save(*args, **kwargs)
        
class Rating(models.Model):
    number = models.ForeignKey(Number, on_delete=models.PROTECT)
    message = models.ForeignKey(Message, on_delete=models.PROTECT)
    rating = models.IntegerField(validators = [MinValueValidator(1), MaxValueValidator(5)])
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
