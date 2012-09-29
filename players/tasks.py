import celery
import requests
import os
import datetime

from StringIO import StringIO

from django.conf import settings

from players.models import Player, BrandFacebookData, BrandTwitterData

@celery.task
def update_player(player_id):
    player = Player.objects.get(id=player_id)
    today = datetime.date.today() - datetime.timedelta(days=1)
    
    if player.brandplayer.twitter_handle:
        params={'screen_name': player.brandplayer.twitter_handle, 'access_token': settings.SINGLY_ACCESS_TOKEN}
        twitter_response = requests.get("https://api.singly.com/proxy/twitter/users/show.json", params=params)
        if twitter_response.status_code == 200:
            twitter_data, created = BrandTwitterData.objects.get_or_create(date=today, player=player)
            twitter_data.followers = twitter_response.json.get('followers_count', 0)
            twitter_data.statused = twitter_response.json.get('statuses_count', 0)
            twitter_data.save()
    
    if player.brandplayer.facebook_name:
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
        
        if player.photo is None:
            photo_request = requests.get('%s/picture' % fb_proxy, params={'access_token': settings.SINGLY_ACCESS_TOKEN, 'type':'large'})
            if photo_request.status_code == 200:
                image_path = os.path.join(settings.MEDIA_ROOT, 'players', '%s.jpeg' % player.id)
                photo_file = open(image_path, 'wb')
                photo_file.write(photo_request.content)
                player.photo = 'players/' +  os.path.basename(image_path)
                player.save()
        