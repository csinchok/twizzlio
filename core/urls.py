from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('twizzlio.core.views',
    url(r'^$', TemplateView.as_view(template_name="index.html"), name="index"),
)