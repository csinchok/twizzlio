import celery
import requests
import os
import datetime

from StringIO import StringIO

from django.conf import settings

from players.models import Player, BrandFacebookData, BrandTwitterData, FacebookData, TwitterData

@celery.task
def update_player(player_id):
    player = Player.objects.get(id=player_id)
    today = datetime.date.today() - datetime.timedelta(days=1)
    
    if hasattr(player, 'brandplayer'):    
        if player.brandplayer.has_twitter():
            params={'screen_name': player.brandplayer.twitter_handle, 'access_token': settings.SINGLY_ACCESS_TOKEN}
            twitter_response = requests.get("https://api.singly.com/proxy/twitter/users/show.json", params=params)
            if twitter_response.status_code == 200:
                twitter_data, created = BrandTwitterData.objects.get_or_create(date=today, player=player)
                twitter_data.followers = twitter_response.json.get('followers_count', 0)
                twitter_data.statused = twitter_response.json.get('statuses_count', 0)
                twitter_data.save()
    
        if player.brandplayer.has_facebook():
            fb_proxy = "https://api.singly.com/proxy/facebook/%s" % player.brandplayer.facebook_name
        
            facebook_response = requests.get(fb_proxy, params={'access_token': settings.SINGLY_ACCESS_TOKEN})
            if facebook_response.status_code == 200:
                fb_data, created = BrandFacebookData.objects.get_or_create(date=today, player=player)
                fb_data.likes = facebook_response.json.get('likes', 0)
                fb_data.talking_about = facebook_response.json.get('talking_about_count', 0)
                fb_data.save()
        
            facebook_response = requests.get("%s/posts" % fb_proxy, params={'limit': 100, 'since':'yesterday', 'access_token': settings.SINGLY_ACCESS_TOKEN})
            if facebook_response.status_code == 200:
                fb_data.posts = len(facebook_response.json.get('data', []))
                fb_data.save()
        
            # if player.photo is None:
            photo_response = requests.get('%s/picture' % fb_proxy, params={'access_token': settings.SINGLY_ACCESS_TOKEN, 'type':'large'})
            if photo_response.status_code == 200:
                store_photo(player, photo_response)
            else:
                print(photo_response.text)
    else:
        access_token = player.user.singly.access_token
        
        if player.has_facebook():
            fb_proxy = "https://api.singly.com/proxy/facebook/me"
            
            facebook_response = requests.get("%s/friends" % fb_proxy, params={'access_token': access_token})
                            
            photo_response = requests.get("%s/picture" % fb_proxy, params={'access_token': access_token, 'type': 'large'})
            if photo_response.status_code == 200:
                store_photo(player, photo_response)
            else:
                print(photo_response.text)
                        
            fb, created = FacebookData.objects.get_or_create(player=player, date=today)
            fb.friends = len(facebook_response.json.get('data', []))
            fb.save()
        
        if player.has_twitter():
            twitter_response = requests.get("https://api.singly.com/profiles/twitter", params={"access_token": access_token})
        
            if twitter_response.status_code == 200:
                
                twitter_data = twitter_response.json.get('data', None)
                if twitter_data:
                    twitter, created = TwitterData.objects.get_or_create(player=player, date=today)
                    twitter.followers = twitter_data.get('followers_count', 0)
                    twitter.statuses = twitter_data.get('statuses_count', 0)
                    twitter.save()

def store_photo(player, photo_response):
    image_path = os.path.join(settings.MEDIA_ROOT, 'players', '%s.jpeg' % player.id)
    photo_file = open(image_path, 'wb')
    photo_file.write(photo_response.content)
    player.photo = 'players/' +  os.path.basename(image_path)
    print(player.photo)
    player.save()
        
        
        
        
        
        
        
        