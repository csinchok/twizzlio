from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

from players.views import PlayerDetailView, PlayerList

urlpatterns = patterns('',
    url(r'^(?P<pk>[0-9]+)$', PlayerDetailView.as_view()),
    url(r'^choose/$', PlayerList.as_view()),
)