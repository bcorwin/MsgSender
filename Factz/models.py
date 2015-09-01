from django.db import models
from random import sample

def rand_code():
    code = sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 1) + sample('1234567890', 4)
    return ''.join(code)
        
class Messages(models.Model):
    message = models.CharField(max_length=320)
    follow_up = models.CharField(max_length=160)
    source = models.CharField(max_length=160)
    count = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    last_sent = models.DateTimeField(blank=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
class Subscriptions(models.Model):
    name = models.CharField(max_length=16)
    active = models.BooleanField()
    last_sent = models.DateTimeField(blank=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
class Numbers(models.Model):
    phone_number = models.CharField(max_length=15)
    subscription_id = models.ForeignKey(Subscriptions)
    message_id = models.ForeignKey(Messages)
    message_cnt = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    last_sent = models.DateTimeField(blank=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
class Unconfirmed(models.Model):
    phone_number = models.CharField(max_length=15)
    confirmation_code = models.CharField(max_length=5, default=rand_code)
    subscription_id = models.ForeignKey(Subscriptions)
    inserted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone_number + " (" + self.confirmation_code + ")"
        
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