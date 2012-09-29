
from django.contrib.auth.models import User
from django.db import models

from players.models import *

# class Game(models.Model):
#     start_time = models.DateTimeField()
#     # duration in minutes
#     duration = models.IntegerField()
# 
# class Roster(models.Model):
#     game = models.ForeignKey(Game)
#     user = models.ForeignKey(User)
#     
#     brand_1 = models.ForeignKey(BrandPlayer)
#     celeb_1 = models.ForeignKey(BrandPlayer)
#     
#     facebook_1 = models.ForeignKey(Player)
#     facebook_2 = models.ForeignKey(Player)
#     
#     twitter_1 = models.ForeignKey(Player)
#     twitter_2 = models.ForeignKey(Player)
#     
#     def compute_score_to_date(self):
#         pass
    