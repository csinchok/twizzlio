# system imports
import csv
import datetime
from random import randrange

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth.models import User

from players.models import *

month_ago = datetime.date(2012, 8, 29)
begin_date = datetime.date(2012, 9, 29)

class Command(BaseCommand):
    def handle(self, *args, **options):    
        for player in Player.objects.select_related('brandplayer').all():
            if player.brandplayer:
                fake_brand(player.brandplayer)
            else:
                fake_player(player)


def fake_brand(player):
    print "Faking %s" % player.name
    earliest_data = BrandTwitterData.objects.filter(player=player).order_by('date')
    
    if earliest_data.count() > 0:
        earliest_data = earliest_data[0]
    
        date = earliest_data.date - datetime.timedelta(days=1)
        last_data = earliest_data
    
        while date > month_ago:
        
            followers = last_data.followers - int(last_data.followers*randrange(-1,1)/200)
            statuses = last_data.statuses - int(last_data.statuses*randrange(0,1)/200)
                
            data = BrandTwitterData.objects.create(player=player,
                date=date, 
                followers=followers,
                statuses=statuses)
        
            last_data = data
            date = date - datetime.timedelta(days=1) 
        
    earliest_data = BrandFacebookData.objects.filter(player=player).order_by('date')
    
    if earliest_data.count() > 0:
        earliest_data = earliest_data[0]
    
        date = earliest_data.date - datetime.timedelta(days=1)
        last_data = earliest_data
    
        while date > month_ago:                
            likes = last_data.likes - int(last_data.likes * (randrange(0,1)/1000))
            talking_about = last_data.talking_about - int(last_data.talking_about * (randrange(-1,1)/1000))
            posts = last_data.posts - randrange(0,10)
                
            data = BrandFacebookData.objects.create(player=player,
                date=date, 
                likes=likes,
                talking_about=talking_about,
                posts=posts)
        
            last_data = data
            date = date - datetime.timedelta(days=1)
    
    
    
def fake_player(player):
    earliest_data = TwitterData.objects.filter(player=player).order_by('date')
    
    if earliest_data.count() > 0:    
        earliest_data = earliest_data[0]
        
        date = earliest_data.date - datetime.timedelta(days=1)
        last_data = earliest_data
    
        while date > month_ago:
        
            followers = last_data.followers - int(last_data.followers*randrange(-1,1)/200)
            statuses = last_data.statuses - int(last_data.statuses*randrange(0,1)/200)
                
            data = TwitterData.objects.create(player=player,
                date=date, 
                followers=followers,
                statuses=statuses)
        
            last_data = data
            date = date - datetime.timedelta(days=1) 
        
    earliest_data = FacebookData.objects.filter(player=player).order_by('date')
    
    if earliest_data.count() > 0:
        earliest_data = earliest_data[0]    
        date = earliest_data.date - datetime.timedelta(days=1)
        last_data = earliest_data
    
        while date > month_ago:                
            friends = last_data.friends - int(last_data.friends * (randrange(0,1)/10))
                
            data = FacebookData.objects.create(player=player,
                date=date, 
                friends=friends)
        
            last_data = data
            date = date - datetime.timedelta(days=1)