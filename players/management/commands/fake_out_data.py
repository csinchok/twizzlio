# system imports
import csv

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth.models import User

from players.models import *

class Command(BaseCommand):
    def handle(self, *args, **options):    
        for player in Player.objects.all():
            if hasattr(player, 'type'):
                fake_brand(player)
            else:
                fake_player(player)


def fake_brand(player):
    
    
def fake_player(player):
    pass