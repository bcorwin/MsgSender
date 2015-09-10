from django.db import models
from random import sample

class Variable(models.Model):
    name = models.CharField(max_length=64, unique=True)
    value = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name + "=" + self.value
    
class Subscription(models.Model):
    name = models.CharField(max_length=16, unique=True)
    active = models.BooleanField()
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
        
def rand_code():
    code = sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 2) + sample('1234567890', 4)
    return ''.join(code)

class Number(models.Model):
    phone_number = models.CharField(max_length=15)
    confirmation_code = models.CharField(max_length=6, default=rand_code)
    message_cnt = models.IntegerField(default=0)
    confirmed = models.BooleanField(default=False)
    last_sent = models.DateTimeField(null=True, blank=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

class activeSubscription(models.Model):
    #Force unique on number_id and subscription_id
    number_id = models.ForeignKey(Number)
    subscription_id = models.ForeignKey(Subscription)
    active = models.BooleanField(default=True)
    last_sent = models.DateTimeField(null=True, blank=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
        
    #To do:
        # On save
            # p_h is in correct format (E.164 format)
            # p_h is not already in the unconfirmed
            # p_h is not already in numbers
            # send confirmation number to number
        # Add a function to confirm a number:
            # check if code = confirmation code
            # if so, move to Numbers and remove from Unconfirmed
        #function to send confirmation to #
        # Clean up unconfirmed numbers that have been in this db for > 1 day
