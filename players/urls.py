from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

from players.views import PlayerList

urlpatterns = patterns('',
    # Examples:
    url(r'^choose/$', PlayerList.as_view()),
)