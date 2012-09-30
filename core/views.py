import requests

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required

from core.models import *

from utils import json_response

# Create your views here.


@login_required
def user_choose(request):
    search = request.GET.get('search', '')
    page = int(request.GET.get('page', 0))
    
    return json_response({
        "page": page,
        "data": [{"id": user.id, "username": user.username, "name": user.get_full_name(), 'photo': "http://placehold.it/40x40"} for user in User.objects.filter(singly__isnull=False, username__contains=search)]
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
    game = get_object_or_404(Game, id=game_id)
        
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
