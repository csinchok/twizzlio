import requests

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from core.models import *

from utils import json_response

# Create your views here.


@login_required
def user_search(request):
    search = request.GET.get('search', '')
    page = int(request.GET.get('page', 0))
    
    return json_response({
        "page": page,
        "data": [{"id": user.id, "name": user.name } for user in User.objects.filter(singly__isnull=False, username__contains=search)]
    })
    
    
@login_required
def create_game(request):
    opponent_id = request.GET.get('opp_id')
    
    try:
        opponent = User.objects.get(id=opponent_id)
    except:
        return json_response({"error": "User Not Found."})
    
    
    game = Game.objects.create(duration=SEVEN_DAYS)
    
    user_roster = Roster.objects.create(game=game, user=request.user)
    opponent_roster = Roster.objects.create(game=game, user=opponent)
    
    return json_response(game.id)
    
@login_required
def game(request, game_id):
    try:
        game = Game.objects.get(game_id)
    except:
        return render_to_response("500.html")
        
    rosters = Roster.objects.filter(game=game)
    
    user_roster = rosters.filter(user=request.user)
    
    return render_to_response("game.html", 
        {"game": game,
         "user_roster": user_roster, 
         "opponent_roster": opponent_roster
        }, context_instance=RequestContext(request))

@login_required
def profile(request):
    
    services = [
        {'name': 'Twitter', 'slug': 'twitter'},
        {'name': 'Facebook', 'slug': 'facebook'},
        {'name': 'Tumblr', 'slug': 'tumblr'},
        {'name': 'Instagram', 'slug': 'instagram'},
        {'name': 'Github', 'slug': 'github'},
    ]
    
    return render_to_response('profile.html',
                              {'services': services},
                              context_instance=RequestContext(request))
