from django.db import models
from bcrypt import checkpw,hashpw,gensalt
from django.core.exceptions import ValidationError

def default_empty_list():
    return []

class users(models.Model):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=17,unique=True,blank=False)
    username = models.CharField(max_length=15, unique=True, blank=False)
    name = models.CharField(max_length=25,blank=False)
    password = models.CharField(max_length=128, blank=False)
    location = models.CharField(max_length=30,default="India", blank=False)
    billing_address = models.JSONField(blank=True, default=default_empty_list)
    order_history = models.JSONField(blank=True, default=default_empty_list)
    favourite_list = models.JSONField(blank=True, default=default_empty_list)

    def __str__(self):
        return self.username
    
    def set_password(self, new_password):
        self.password = hashpw(new_password.encode('utf-8'),gensalt()).decode('utf-8')
        self.save()

    def check_password(self, old_passowrd):
        
        if checkpw(old_passowrd.encode('utf-8'),
                    self.password.encode('utf-8')):
            return True
        else:
            return False
        