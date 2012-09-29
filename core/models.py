import datetime

from django.contrib.auth.models import User
from django.db import models

from players.models import *

class Game(models.Model):
    start_time = models.DateTimeField()
    # duration in minutes
    duration = models.IntegerField()
    is_active = models.BooleanField(default=False)

class Roster(models.Model):
    game = models.ForeignKey(Game)
    user = models.ForeignKey(User)
    
    celeb_1 = models.ForeignKey(BrandPlayer, related_name="celeb")
    brand_1 = models.ForeignKey(BrandPlayer, related_name="brand")
    
    facebook_1 = models.ForeignKey(Player, related_name="facebook_1")
    facebook_2 = models.ForeignKey(Player, related_name="facebook_2")
    
    twitter_1 = models.ForeignKey(Player, related_name="twitter_1")
    twitter_2 = models.ForeignKey(Player, related_name="twitter_2")
    
    def get_scores(self):
        start_date = self.game.start_time.date()
        today = datetime.date.today()
        vals =  {
            "celeb_1": self.celeb_1.score(start_date, today),
            "brand_1": self.brand_1.score(start_date, today),
            "facebook_1": self.facebook_1.score(start_date, today, FacebookData),
            "facebook_2": self.facebook_2.score(start_date, today, FacebookData),
            "twitter_1": self.twitter_1.score(start_date, today, TwitterData),
            "twitter_2": self.twitter_2.score(start_date, today, TwitterData),
        }
        
        vals['total'] = sum([value for key, value in vals.items()])
        
        return vals
        
    