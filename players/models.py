import datetime
import requests

from django.db import models

singly_url = "https://api.singly.com/"
proxy = "https://api.singly.com/proxy/facebook/"

class Player(models.Model):
    name = models.CharField(max_length=255)
    # brand, celeb, or normal
    photo = models.URLField()
    
    user = models.ForeignKey(User, null=True)
    
    def score(self, date, service):
        if self.type == "brand" or self.type == "celeb":
            pass
        else:
            pass

class CelebPlayer(Player):
    twitter = models.CharField(max_length=255)
    facebook = models.CharField(max_length=255)
    
    def import_facebook(self):
        facebook = self.facebook
        r = requests.get("%s/%s?access_token=" % proxy, facebook, settings.SINGLY_ACCESS_TOKEN)
        
        likes = r.json['likes']
        talking_about = r.json['talking_about_count']
        
        r = requests.get("%s/%s/posts?limit=100&since=yesterday&access_token=%s" % (proxy, name, settings.SINGLY_ACCESS_TOKEN))
        
        posts = len(r.posts['data'])
        
        today = datetime.date.today() - datetime.timedelta(days=1)

        FacebookCelebService.objects.get_or_create(date=today, 
            player=self, 
            likes_count=likes,
            talking_about_count=talking_about,
            posts_count=posts)
        
        
    def import_twitter(celeb):
        pass

class Service(models.Model):
    player = models.ForeignKey(Player)
    date = models.DateField()
    
    class Meta:
        abstract = True   
        unique_together = ('player', 'date') 
        
    
class CelebFacebookService(Service):
    likes = models.IntegerField()
    talking_about = models.IntegerField()
    posts = models.IntegerField()
    
    def get_score(self):
        pass
        
class FacebookService(Service):    
    # what do we want to do for this
    friend_count = models.IntegerField()
    
    def get_score(self):
        pass

# class TwitterService(Service):
#     # what do we want to do for this
#     follower_count = models.IntegerField()
#     
#     def compute_score():
#         pass
        
# class CelebTwitterService(Service):
#     follower_count = models.IntegerField()
    
    
    
     
    
    