from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('core.views',
    url(r'^$', TemplateView.as_view(template_name="index.html"), name="index"),
    url(r'^new$', TemplateView.as_view(template_name="new.html"), name="new"),

    #listing of matchups
    # url(r'^matchups$', TemplateView.as_view(template_name="matchups.html"), name="matchups"), 

    url(r'^matchups$', 'matchups'),


    #head to head view
    url(r'^game/(?P<game_id>\d+)$', 'game'),

    url(r'^about$', TemplateView.as_view(template_name="about.html"), name="about"),
    url(r'^welcome$', TemplateView.as_view(template_name="welcome.html"), name="welcome"),
    
    url(r'^users/choose/$', 'user_choose'),
    url(r'^create_game/$', 'create_game'),
    url(r'^roster/fill_slot$', 'fill_slot'),
    url(r'^roster/empty_slot$', 'empty_slot'),
    
    url(r'^corporate$', TemplateView.as_view(template_name="corporate.html"), name="corporate"),
    url(r'^investors$', TemplateView.as_view(template_name="investors.html"), name="investors"),
    url(r'^brands$', TemplateView.as_view(template_name="brands.html"), name="brands"),
    url(r'^profile$', 'profile'),
)