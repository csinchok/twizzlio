import json

import datetime

from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import HttpResponse

from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from sorl.thumbnail import get_thumbnail

from players.models import *

from utils import json_response

class PlayerDetailView(DetailView):
    
    model = Player
    
    def get_context_data(self, **kwargs):
        context = super(PlayerDetailView, self).get_context_data(**kwargs)
        
        start_date = datetime.datetime.now() - datetime.timedelta(weeks=2)
        scores = []
        for day in xrange(14):
            if hasattr(self.object, 'brandplayer'):
                score = self.object.brandplayer.score(start_date)
                scores.append({
                    'date': start_date.strftime('%m/%d'),
                    'facebook': score.get('facebook', 0),
                    'twitter': score.get('twitter', 0),
                })
            else:
                score = self.object.score(start_date)
                scores.append({
                    'date': start_date.strftime('%m/%d'),
                    'facebook': score.get('facebook', 0),
                    'twitter': score.get('twitter', 0),
                })
            start_date = start_date + datetime.timedelta(days=1)
        context['scores'] = scores
        return context

class PlayerList(ListView):
    model = Player
    
    def get_queryset(self):
        request = self.request
        
        if not self.request.user.is_authenticated():
            return []
    
        player_type = request.GET.get('type', None)
        search = request.GET.get('search', '')
        page = int(request.GET.get('page', 1))
        
        search_kwargs = {'name__icontains': search}
        
        if player_type == "facebook":
            search_kwargs['has_facebook'] = True
        elif player_type == "twitter":
            search_kwargs['has_twitter'] = True
        elif player_type == "brands":
            search_kwargs['brandplayer__type'] = BrandPlayer.BRAND            
        elif player_type == "celebs":
            search_kwargs['brandplayer__type'] = BrandPlayer.CELEB
            
        players = Player.objects.filter(**search_kwargs)
         
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
                     "photo": get_thumbnail(player.photo, '40x40', crop='center').url} for player in context['object_list']]}
        
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(
            json.dumps(pages),
            **response_kwargs
        )
    
    
        