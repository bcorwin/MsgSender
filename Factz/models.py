from django.db import models
from random import sample

class Variable(models.Model):
    name = models.CharField(max_length=64, unique=True)
    value = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name + "=" + self.value
    
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
    
    def save(self, *args, **kwargs):
        phone_number = str(self.phone_number)
        phonePattern = re.compile(r'^\D*\+{0,1}1{0,1}\D*(\d{3})\D*(\d{3})\D*(\d{4}).*$', re.VERBOSE)
        if phonePattern.match(phone_number):
            grps = phonePattern.search(phone_number).groups()
            self.phone_number = "+1" + ''.join(grps[0:3])
        else:
            raise ValueError(phone_number + " is not a valid phone number format.")
        # To do: send a test text message (or just send the confirmation message here?)
        # to validate that the number can recieve texts
        super(Number, self).save(*args, **kwargs)
    
    class Meta:
        unique_together = ('phone_number')
        
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
