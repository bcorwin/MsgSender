from django.db import models
from Factz.do import rand_code, format_number
from Factz.messaging import send_test_message

class Variable(models.Model):
    name = models.CharField(max_length=64, unique=True)
    val = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name + "=" + self.val
    
class Subscription(models.Model):
    name = models.CharField(max_length=16, unique=True)
    active = models.BooleanField(default=True)
    last_sent = models.DateTimeField(null=True, blank=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Message(models.Model):
    message = models.CharField(max_length=320)
    follow_up = models.CharField(max_length=160, blank=True, null=True)
    source = models.CharField(max_length=160, blank=True, null=True)
    subscription_id = models.ForeignKey(Subscription)
    count = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    last_sent = models.DateTimeField(null=True, blank=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
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
    
    def save(self, *args, **kwargs):
        self.phone_number = format_number(self.phone_number)
        
        chk = send_test_message(message_text="test", to_number=phone_number)
        if chk[0] != 0:
            raise ValueError(chk[1])
		
        super(Number, self).save(*args, **kwargs)
		
    def __str__(self):
        return self.phone_number
        
class activeSubscription(models.Model):
    number_id = models.ForeignKey(Number)
    subscription_id = models.ForeignKey(Subscription)
    message_id = models.ForeignKey(Message, blank=True, null=True)
    message_cnt = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    last_sent = models.DateTimeField(null=True, blank=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('number_id', 'subscription_id')
        
    #To do:
        # Add a function to confirm a number:
            # check if code = confirmation code
            # if so, move to Numbers and remove from Unconfirmed
        #function to send confirmation to #
        # Clean up unconfirmed numbers that have been in this db for > 1 day
