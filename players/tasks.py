import celery
import requests

from django.conf import settings

from players.models import Player

SINGLY_URL = "https://api.singly.com/"
FB_PROXY = "https://api.singly.com/proxy/facebook/"
TWITTER_PROXY = "https://api.singly.com/proxy/twitter/"

@celery.task
def update_player(player_id):
    player = Player.objects.get(id=player_id)
    
    if player.facebook_name:
        fb_data, created = BrandFacebookData.objects.get_or_create(date=today, player=self)
        
        
        fb_proxy = "https://api.singly.com/proxy/facebook/%s" % player.facebook_name
        
        facebook_response = requests.get(fb_proxy, params={'access_token': settings.SINGLY_ACCESS_TOKEN})
        if facebook_response.status_code == 200:
            fb_data.likes = facebook_response.json.get('likes', 0)
            fb_data.talking_about = facebook_response.json.get('talking_about_count', 0)
            fb_data.save()
        
        facebook_response = requests.get("%s/posts" % fb_proxy, params={'limit': 100, 'since':'yesterday', 'access_token': settings.SINGLY_ACCESS_TOKEN})
        if facebook_response.status_code == 200:
            fb_data.posts = len(r.json.get('data', []))
            fb_data.save()
        
        if player.photo is None:
            try:
                redirect = requests.get('%s/picture' % fb_proxy, params={'access_token': settings.SINGLY_ACCESS_TOKEN, 'type':large})
                player.photo = url
                player.save()
            except:
                pass