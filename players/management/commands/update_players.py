# system imports

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from players.models import Player
from players.tasks import update_player

class Command(BaseCommand):
    def handle(self, *args, **options):
        for player in Player.objects.all():
            update_player.delay(player.id)