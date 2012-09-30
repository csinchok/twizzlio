from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from players.models import *

from utils import json_response

@login_required
def choose(request):
    user = request.user
    
    player_type = request.GET.get('type', None)
    search = request.GET.get('search', '')
    page = int(request.GET.get('page', 0))
    
    if page < 0:
        page = 0
    
    if player_type == "facebook":
        players = Player.objects.filter(has_facebook=True)
    elif player_type == "twitter":
        players = Player.objects.filter(has_twitter=True)
    elif player_type == "brands":
        players = BrandPlayer.objects.filter(type=BrandPlayer.BRAND)
    elif player_type == "celebs":
        players = BrandPlayer.objects.filter(type=BrandPlayer.CELEB)
    else:
        players = Player.objects.all()
    
    players = players.filter(name__contains=search)[(page * 5):(page * 5 + 5)]
    
    return json_response({
        "page": page,
        "data": [{"id": player.id, "name": player.name, "photo": player.photo.url } for player in players]
    })
    
    
    
        