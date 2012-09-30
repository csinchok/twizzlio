# system imports
import csv
import datetime
from random import randrange

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth.models import User

from players.models import *

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
        
        month_ago = date - datetime.timedelta(days=30)
    
        while date > month_ago:
        
            followers = last_data.followers - int(last_data.followers * (float(randrange(0,10))/1000))
            statuses = last_data.statuses - int(last_data.statuses * (float(randrange(0,10))/1000))
                
            print date, followers, statuses    
            
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
        
        month_ago = date - datetime.timedelta(days=30)
    
        while date > month_ago:                
            likes = last_data.likes - int(last_data.likes * (float(randrange(0,10))/1000))
            talking_about = last_data.talking_about - int(last_data.talking_about * (float(randrange(0,10))/1000))
            posts = last_data.posts + randrange(-1,1)
            
            print date, likes, talking_about, posts
                
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
        
        month_ago = date - datetime.timedelta(days=30)
    
        while date > month_ago:
        
            followers = last_data.followers - int(last_data.followers * (float(randrange(-1,1))/200))
            statuses = last_data.statuses - int(last_data.statuses * (float(randrange(0,1))/200))
                
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
        
        month_ago = date - datetime.timedelta(days=30)
    
        while date > month_ago:                
            friends = last_data.friends - randrange(0,2)
                
            data = FacebookData.objects.create(player=player,
                date=date, 
                friends=friends)
        
            last_data = data
            date = date - datetime.timedelta(days=1)