# system imports
import csv

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth.models import User

from players.models import *
from players.tasks import update_player

class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.filter(player__isnull=True, is_superuser=False)
        
        for user in users:
            player = Player.objects.create(user=user,name=user.first_name)
            update_player.delay(player.id)