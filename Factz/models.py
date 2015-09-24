from django.db import models
from Factz.utils import rand_code, format_number
from Factz.messaging import send_test_message, send_message
from django.utils import timezone

class Variable(models.Model):
    name = models.CharField(max_length=64, unique=True)
    val = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name + "=" + self.val
    
class Subscription(models.Model):
    name = models.CharField(max_length=16, unique=True)
    active = models.BooleanField(default=True)
    count = models.IntegerField(default=0)
    last_sent = models.DateTimeField(null=True, blank=True)
    next_send = models.DateTimeField(null=True, blank=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def update_sent(self):
        self.last_sent = timezone.now()
        self.count += 1
        self.save()
        
    def __str__(self):
        return self.name

class Message(models.Model):
    message = models.CharField(max_length=320)
    follow_up = models.CharField(max_length=160, blank=True, null=True)
    source = models.CharField(max_length=160, blank=True, null=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.PROTECT)
    count = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    last_sent = models.DateTimeField(null=True, blank=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def update_sent(self):
        self.count += 1
        self.last_sent = timezone.now()
        self.save()
    
    def __str__(self):
        return self.message

class Number(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    confirmation_code = models.CharField(max_length=6, default=rand_code)
    message_cnt = models.IntegerField(default=0)
    confirmed = models.BooleanField(default=False)
    last_sent = models.DateTimeField(null=True, blank=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def update_sent(self):
        self.last_sent = timezone.now()
        self.message_cnt += 1
        self.save()
    
    def create(self, *args, **kwargs):
        self.phone_number = format_number(self.phone_number)
        
        chk = send_test_message(self)
        if chk[0] != 0:
            raise ValueError(chk[1])
		
    def __str__(self):
        return self.phone_number
        
class activeSubscription(models.Model):
    number = models.ForeignKey(Number, on_delete=models.PROTECT)
    subscription = models.ForeignKey(Subscription, on_delete=models.PROTECT)
    message = models.ForeignKey(Message, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    message_cnt = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    last_sent = models.DateTimeField(null=True, blank=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def update_sent(self, msgObj):
        self.message = msgObj
        self.message_cnt += 1
        self.last_sent = timezone.now()
        self.number.update_sent()
        self.save()
    
    def send(self, msgObj):
        if self.active == True:
            res = send_message(msgObj, self)
            if res[0] == 0:
                self.update_sent(msgObj)
                if msgObj.follow_up != None:
                    send_message(msgObj, self, type="followup")
        else:
            res = (2, "Not active.")
        return res
    
    class Meta:
        unique_together = ('number', 'subscription')
    
    def __str__(self):
        return str(self.number) + " " + str(self.subscription) + " (" + str(self.active) + ")"
