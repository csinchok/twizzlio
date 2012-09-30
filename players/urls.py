from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

from players.views import PlayerDetailView

urlpatterns = patterns('players.views',
    (r'^choose/$', 'choose'),
    url(r'^(?P<pk>[0-9]+)$', PlayerDetailView.as_view()),
)