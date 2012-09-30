import requests

from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from players.models import Player


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