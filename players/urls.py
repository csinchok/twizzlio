from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('players.views',
    # Examples:
    url(r'^choose/$', 'choose'),
)