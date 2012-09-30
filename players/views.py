import json

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import HttpResponse

from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from players.models import *

from utils import json_response


class PlayerList(ListView):
    model = Player
    
    def get_queryset(self):
        request = self.request
        
        if not self.request.user.is_authenticated():
            return []
    
        player_type = request.GET.get('type', None)
        search = request.GET.get('search', '')
        page = int(request.GET.get('page', 1))
        
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
            
        players = players.filter(name__icontains=search)
         
        paginator = Paginator(players, 5)
            
        try:
            p = paginator.page(page)
        except PageNotAnInteger:
            p = paginator.page(1)
        except EmptyPage:
            p = paginator.page(paginator.num_pages)
        
        return p         
    
    def render_to_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        
        pages = { "page": context['object_list'].number,
                  "data": [{
                     "id": player.id, 
                     "name": player.name, 
                     "photo": player.photo.url} for player in context['object_list']]}
        
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(
            json.dumps(pages),
            **response_kwargs
        )
    
    
    
        