# models.py

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import random
import string


def generate_report_id(length=10):
    chars = string.ascii_uppercase + string.digits  # A-Z + 0-9
    return ''.join(random.choices(chars, k=length))

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

# class Analysis(models.Model):
#     number_of_plants = models.IntegerField()
#     branches_per_plant = models.IntegerField()
#     desired_goals = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)

# class AnalysisImage(models.Model):
#     analysis = models.ForeignKey(Analysis, related_name='images', on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='analysis_images/')
#     ai_response = models.TextField(blank=True, null=True)  
#     uploaded_at = models.DateTimeField(auto_now_add=True)
    
    
    
#this part can be separated
# this is standard that we must follow everywhere

class Analysis(models.Model):
    PEAK_POTENCY = 1
    DESIRED_EFFECTS = 2
    YIELD_OPTIMIZATION = 3

    CAPTURE_WITH_CAMERA = 1
    UPLOAD_FROM_DEVICE = 2

    STATE_1 = 1
    STATE_2 = 2
    STATE_3 = 3

    TYPE_1 = 1
    TYPE_2 = 2
    DESIRED_GOAL_CHOICES = [
        (PEAK_POTENCY, 'Peak Potency'),
        (DESIRED_EFFECTS, 'Desired Effects'),
        (YIELD_OPTIMIZATION, 'Yield Optimization'),
    ]
    
    STATE_CHOICES = [
        (STATE_1, 'State 1'),
        (STATE_2, 'State 2'),
        (STATE_3, 'State_added_to_grow_logs'),
    ]

    TYPE_CHOICES = [
        (TYPE_1, 'Type 1'),
        (TYPE_2, 'Type 2'),
    ]
   

    number_of_plants = models.IntegerField()
    branches_per_plant = models.IntegerField()
    desired_goal = models.IntegerField(choices=DESIRED_GOAL_CHOICES)
    image_file = models.ImageField(null=True, blank=True, upload_to='analysis_files/')
    state_id = models.IntegerField(choices=STATE_CHOICES)
    type_id = models.IntegerField(choices=TYPE_CHOICES)
    analysis_result = models.TextField(null=True, blank=True)
    raw_result = models.TextField(null=True, blank=True)
    created_by_id = models.IntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True) 
    report_id = models.CharField(max_length=20, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(default=timezone.now)  # Provide a default value
    updated_at = models.DateTimeField(auto_now=True)
    strain_name = models.TextField(null=True, blank=True)
    thc_estimate = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.report_id:
            self.report_id = generate_report_id()
        super().save(*args, **kwargs)

    def __str__(self):
            return f"Analysis {self.id}"
