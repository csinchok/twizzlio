from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('twizzlio.core.views',
    url(r'^$', TemplateView.as_view(template_name="index.html"), name="index"),
    url(r'^new$', TemplateView.as_view(template_name="new.html"), name="new"),

    #listing of matchups
    url(r'^matchups$', TemplateView.as_view(template_name="matchups.html"), name="matchups"), 

    #head to head view
    url(r'^game$', TemplateView.as_view(template_name="game.html"), name="game"),


    url(r'^about$', TemplateView.as_view(template_name="about.html"), name="about"),

    url(r'^welcome$', TemplateView.as_view(template_name="welcome.html"), name="welcome"),
    url(r'^profile$', TemplateView.as_view(template_name="profile.html"), name="profile"),


)