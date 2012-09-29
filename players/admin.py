from django.contrib import admin
from players.models import *

admin.site.register(Player)
admin.site.register(BrandPlayer)

admin.site.register(BrandFacebookData)
admin.site.register(FacebookData)
admin.site.register(TwitterData)
admin.site.register(BrandTwitterData)