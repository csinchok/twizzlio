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
            
    def score(self, date):
        date_before = date - datetime.timedelta(days=1)
        score = {}
        if self.has_twitter():
            try:
                second_day = TwitterData.objects.get(player=self, date=date)
                first_day = TwitterData.objects.get(player=self, date=date_before)
            except TwitterData.DoesNotExist:
                score['twitter'] = 0
            else:
                score['twitter'] = second_day.compute_score() - first_day.compute_score()
        
        if self.has_facebook():
            try:
                second_day = FacebookData.objects.get(player=self, date=date)
                first_day = FacebookData.objects.get(player=self, date=date_before)
            except FacebookData.DoesNotExist:
                score['facebook'] = 0
            else:
                score['facebook'] = second_day.compute_score() - first_day.compute_score()
        
        return score    

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
        
    def score(self, date):
        date_before = date - datetime.timedelta(days=1)
        score = {}
        if self.has_twitter():
            try:
                second_day = BrandTwitterData.objects.get(player=self, date=date)
                first_day = BrandTwitterData.objects.get(player=self, date=date_before)
            except BrandTwitterData.DoesNotExist:
                score['twitter'] = 0
            else:
                base_score = first_day.compute_score()
                if base_score == 0:
                    # if base is zero, just take absolute score
                    score['twitter'] = second_day.compute_score()
                else:
                    # 10x percent change
                    score['twitter'] = 1000 * (float(second_day.compute_score() - base_score)/base_score)
        
        if self.has_facebook():
            try:
                second_day = BrandFacebookData.objects.get(player=self, date=date)
                first_day = BrandFacebookData.objects.get(player=self, date=date_before)
            except BrandFacebookData.DoesNotExist:
                score['facebook'] = 0
            else:
                base_score = first_day.compute_score()
                if base_score == 0:
                    # if base is zero, just take absolute score
                    score['facebook'] = second_day.compute_score()
                else:
                    # 10x percent change
                    score['facebook'] = 1000*(float(second_day.compute_score() - base_score)/base_score)
        
        return score
        
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
    
    
     
    
    