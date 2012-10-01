import datetime
import requests

from math import log

from django.conf import settings
from django.contrib.auth.models import User

from django.db import models
from django.db.utils import IntegrityError

singly_url = "https://api.singly.com/"
fb_proxy = "https://api.singly.com/proxy/facebook/"
twitter_proxy = "https://api.singly.com/proxy/twitter/"

class Player(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='player', null=True, blank=True)
    
    user = models.ForeignKey(User, null=True, blank=True)
    
    def has_twitter(self):
        return self.user and self.user.singly and ("twitter" in self.user.singly.services())
        
    def has_facebook(self):
        return self.user and self.user.singly and ("facebook" in self.user.singly.services())
    
    def score_average(self, start_date, end_date, Service):
        datum = Service.objects.filter(player=self, date__gte=start_date, date__lte=end_date)
        if datum:
            total = 0
            for data in datum:
                total += data.compute_score()
            return total / datum.count()
        return total
    
    def score(self, start_date, end_date, Service):
        try:
            start_service = Service.objects.get(player=self, date=start_date.date)
            end_service = Service.objects.get(player=self, date=end_date.date)
            return end_service.compute_score() - start_service.compute_score()
        except:
            return 0        
    
    def __unicode__(self):
        return self.name
                
    class Meta:
        unique_together = ('name', 'user')

class BrandPlayer(Player):
    # Constants
    BRAND = 0
    CELEB = 1

    PLAYER_CHOICES = (
        (BRAND, 'Brand'),
        (CELEB, 'Celeb')
    )
    
    # brand or celeb
    type = models.IntegerField(default=BRAND, choices=PLAYER_CHOICES)
    
    twitter_handle = models.CharField(max_length=255)
    facebook_name = models.CharField(max_length=255)
    
    def has_twitter(self):
        return self.twitter_handle
        
    def has_facebook(self):
        return self.facebook_name
    
    def score(self, start_date, end_date):
        try:
            start_facebook = BrandFacebookData.objects.get(player=self, date=start_date)
            end_facebook = BrandFacebookData.objects.get(player=self, date=end_date)
            facebook_score = end_facebook.compute_score() - start_facebook.compute_score()
        except:
            facebook_score = 0
            
        try:
            start_twitter = BrandTwitterData.objects.get(player=self, date=start_date)
            end_twitter = BrandTwitterData.objects.get(player=self, date=end_date)
            twitter_score = end_twitter.compute_score() - start_twitter.compute_score()
        except:
            twitter_score = 0
            
        return log(facebook_score + twitter_score)
            
    def str(self):
        return self.name
        
        

class ServiceData(models.Model):
    player = models.ForeignKey(Player)
    date = models.DateField()
    
    class Meta:
        abstract = True   
        unique_together = ('player', 'date') 
        
        
class BrandFacebookData(ServiceData):
    likes = models.IntegerField(null=True)
    talking_about = models.IntegerField(null=True)
    posts = models.IntegerField(null=True)
    
    def compute_score(self):
        return self.likes + self.talking_about + self.posts
        
class FacebookData(ServiceData):    
    friends = models.IntegerField(null=True)
    
    def compute_score(self):
        return self.friends

class TwitterData(ServiceData):
    followers = models.IntegerField(null=True)
    statuses = models.IntegerField(null=True)
    
    def compute_score(self):
        return self.followers + self.statuses
        
class BrandTwitterData(ServiceData):
    followers = models.IntegerField(null=True)
    statuses = models.IntegerField(null=True)
    
    def compute_score(self):
        return self.followers + self.statuses
    
    
     
    
    