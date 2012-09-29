import datetime
import requests

from django.conf import settings
from django.db import models
from django.db.utils import IntegrityError

singly_url = "https://api.singly.com/"
fb_proxy = "https://api.singly.com/proxy/facebook/"
twitter_proxy = "https://api.singly.com/proxy/twitter/"

class Player(models.Model):
    name = models.CharField(max_length=255)
    photo = models.URLField(null=True)
    
    user_id = models.IntegerField(null=True)
    
    def score(self, date, service):
        if self.type == "brand" or self.type == "celeb":
            pass
        else:
            pass
            
    class Meta:
        unique_together = ('name', 'user_id')

class BrandPlayer(Player):
    twitter_handle = models.CharField(max_length=255)
    # brand or celeb
    type = models.CharField(max_length=10)
    facebook_name = models.CharField(max_length=255)
    
    def import_facebook(self):
        if self.facebook_name is None:
            return
            
        r = requests.get("%s%s?access_token=%s" % (fb_proxy, self.facebook_name, settings.SINGLY_ACCESS_TOKEN))
        
        likes = r.json['likes']
        talking_about = r.json['talking_about_count']
        
        if self.photo is None:
            url = "%s%s/picture?type=large&access_token=%s" % (fb_proxy, self.facebook_name, settings.SINGLY_ACCESS_TOKEN)
            self.photo = url
            self.save()
        
        r = requests.get("%s/%s/posts?limit=100&since=yesterday&access_token=%s" % (fb_proxy, self.facebook_name, settings.SINGLY_ACCESS_TOKEN))
        
        posts = len(r.json['data'])
        
        today = datetime.date.today() - datetime.timedelta(days=1)

        fb_data, created = BrandFacebookData.objects.get_or_create(date=today, player=self)
        fb_data.likes = likes
        fb_data.talking_about = talking_about
        fb_data.posts = posts
        fb_data.save()
        
        
    def import_twitter(self):
        if self.twitter_handle is None:
            return
            
        r = requests.get("%susers/show.json?screen_name=%s&access_token=%s" % (twitter_proxy, self.twitter_handle, settings.SINGLY_ACCESS_TOKEN))
        followers = r.json['followers_count']
        statuses = r.json['statuses_count']
        
        # r = requests.get("%sstatuses/user_timeline.json?count=200&screen_name=%s&access_token=%s" % (twitter_proxy, self.twitter_handle, settings.SINGLY_ACCESS_TOKEN))
        
        today = datetime.date.today() - datetime.timedelta(days=1)
        
        twitter_data, created = BrandTwitterData.objects.get_or_create(date=today, player=self)
            
        twitter_data.statuses = statuses
        twitter_data.followers = followers
        twitter_data.save()
            
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
    # what do we want to do for this
    friend_count = models.IntegerField(null=True)
    
    def compute_score(self):
        pass

class TwitterData(ServiceData):
    followers = models.IntegerField(null=True)
    statuses = models.IntegerField(null=True)
    
    def compute_score(self):
        pass
        
class BrandTwitterData(ServiceData):
    followers = models.IntegerField(null=True)
    statuses = models.IntegerField(null=True)
    
    def compute_score(self):
        return self.followers + self.statuses
    
    
     
    
    