import datetime
import requests

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
    
    has_twitter = models.BooleanField(default=False)
    has_facebook = models.BooleanField(default=False)
    
    user = models.ForeignKey(User, null=True, blank=True)
    
    def score_average(self, start_date, end_date, Service):
        datum = Service.objects.filter(player=self, date__gte=start_date, date__lte=end_date)
        total = 0
        for data in datum:
            total+= data.compute_score()
        return total / datum.count()
    
    def score(self, start_date, end_date, Service):
        try:
            start_service = Service.objects.get(player=self, date=start_date.date)
            end_service = Service.objects.get(player=self, date=end_date.dates)
            return end_service - start_service
        except:
            return 0   
            
            
    def import_facebook(self, date=datetime.date.today()):
        access_token = self.user.singly.access_token
        
        r = requests.get("%sme/friends?access_token=%s" % (fb_proxy, access_token))
        
        friends = len(r.json.get('data', []))
            
        if self.photo is None:
            try:
                url = "%sme/picture?type=large&access_token=%s" % (fb_proxy, self.facebook_name, settings.SINGLY_ACCESS_TOKEN)
                self.photo = url
                self.save()
            except:
                pass
                        
        fb, created = FacebookData.objects.get_or_create(player=self, date=date)
        fb.friends = friends
        fb.save()
    
    def import_twitter(self, date=datetime.date.today()):
        access_token = self.user.singly.access_token
        
        r = requests.get("%sprofiles/twitter?access_token=%s" % (singly_url, access_token))
        
        data = r.json.get('data', None)
        
        if not data:
            return
        
        followers = data.get('followers_count', 0)
        statuses = data.get('statuses_count', 0)
            
        twitter, created = TwitterData.objects.get_or_create(player=self, date=date)
        twitter.followers = followers
        twitter.statuses = statuses
        twitter.save()
        
    def save(self, *args, **kwargs):
        if self.user:
            access_token = self.user.singly.access_token
        
            r = requests.get("%sv0/profile?access_token=%s" % (singly_url, access_token))
                
            photo = r.json.get("thumbnail_url", None)
            if photo:
                self.photo = photo
            
            services = r.json.get("services", None)
            if services:
                if services.get("twitter", None):
                    self.has_twitter = True
                if services.get("facebook", None):
                    self.has_facebook = True
                
        super(Player, self).save(*args, **kwargs)
    
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
            
        return facebook_score + twitter_score
            
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
    
    
     
    
    