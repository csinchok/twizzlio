import datetime

from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from players.models import *

from utils import json_response

class PlayerDetailView(DetailView):
    
    model = Player
    
    def get_context_data(self, **kwargs):
        context = super(PlayerDetailView, self).get_context_data(**kwargs)
        
        start_date = datetime.datetime.now() - datetime.timedelta(weeks=2)
        scores = []
        for day in xrange(14):
            end_date = start_date + datetime.timedelta(days=1)
            if self.object.brandplayer:
                scores.append({
                    'date': start_date.strftime('%m/%d'),
                    'facebook': self.object.score(start_date, end_date, BrandFacebookData),
                    'twitter': self.object.score(start_date, end_date, BrandTwitterData),
                })
            else:
                scores.append({
                    'date': start_date.strftime('%m/%d'),
                    'facebook': self.object.score(start_date, end_date, FacebookData),
                    'twitter': self.object.score(start_date, end_date, TwitterData),
                })
            start_date = end_date
        context['scores'] = scores
        return context


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
    
    
    
        