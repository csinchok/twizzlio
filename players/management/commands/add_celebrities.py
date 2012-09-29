# system imports
import csv

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from players.models import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        reader = csv.reader(open('celebs.csv', 'r'))
                
        for line in reader:
            if line[0] == "Brand":
                continue
            facebook_name = line[2].split("/")[-1]
            
            celeb, created = BrandPlayer.objects.get_or_create(name=line[0], twitter_handle=line[1], type="celeb", facebook_name=facebook_name)
            celeb.import_facebook()
            celeb.import_twitter()