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
        
        facebook_response = requests.get("%s%s?access_token=%s" % (fb_proxy, player.facebook_name, settings.SINGLY_ACCESS_TOKEN))