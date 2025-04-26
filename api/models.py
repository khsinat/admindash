# models.py

from django.db import models
from django.contrib.auth import get_user_model

class ContactUs(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    contact_no = models.CharField(max_length=15, blank=True, null=True)  # Add this line
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Page(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    state_id = models.IntegerField(default=1)
    type_id = models.IntegerField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

PAGE_TYPE_TERMS_AND_CONDITIONS = 2
 
PAGE_TYPE_PRIVACY_POLICY = 1

    
class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500, unique=True)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token
    

#constants

STATE_ACTIVE = 0
    
STATE_INACTIVE = 1    
    
STATE_DELETED = 2


class Package(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

