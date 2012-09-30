import datetime

from django.contrib.auth.models import User
from django.db import models

from players.models import *

SEVEN_DAYS = 7*24*60*60

class Game(models.Model):
    start_time = models.DateTimeField(null=True, blank=True)
    # duration in minutes
    duration = models.IntegerField()
    is_active = models.BooleanField(default=False)
    
    def __unicode__(self):
        return " vs. ".join([roster.user.get_full_name() for roster in self.roster_set.all()])

class Roster(models.Model):
    game = models.ForeignKey(Game)
    user = models.ForeignKey(User)
    
    celeb_1 = models.ForeignKey(BrandPlayer, related_name="celeb", null=True, blank=True)
    brand_1 = models.ForeignKey(BrandPlayer, related_name="brand", null=True, blank=True)
    
    facebook_1 = models.ForeignKey(Player, related_name="facebook_1", null=True, blank=True)
    facebook_2 = models.ForeignKey(Player, related_name="facebook_2", null=True, blank=True)
    
    twitter_1 = models.ForeignKey(Player, related_name="twitter_1", null=True, blank=True)
    twitter_2 = models.ForeignKey(Player, related_name="twitter_2", null=True, blank=True)
    
    instagram_1 = models.ForeignKey(Player, related_name="instagram_1", null=True, blank=True)
    tumblr_1 = models.ForeignKey(Player, related_name="tumblr_1", null=True, blank=True)
        
    def is_full(self):
        return self.celeb_1 is not None and self.brand_1 is not None and self.facebook_1 is \
            not None and self.facebook_2 is not None and self.twitter_1 is not None \
            and twitter_2 is not None
    
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
        
    