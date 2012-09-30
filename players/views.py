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
                    'facebook': self.object.score_average(start_date, end_date, BrandFacebookData),
                    'twitter': self.object.score_average(start_date, end_date, BrandTwitterData),
                })
            else:
                scores.append({
                    'date': start_date.strftime('%m/%d'),
                    'facebook': self.object.score_average(start_date, end_date, FacebookData),
                    'twitter': self.object.score_average(start_date, end_date, TwitterData),
                })
            start_date = end_date
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
    
    
        