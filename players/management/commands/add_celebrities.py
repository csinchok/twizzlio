# system imports
import calendar
import codecs
import datetime
import httplib2
from optparse import make_option
import re
import sys

from django.conf import settings

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        if len(args) >= 1 and (args[0] == "onion" or args[0] == "avclub"):
            site = args[0]
            if site == "onion":
                calculate_pace(OnionContentType, OnionPage, OnionPageData, OnionPace)
            else:
                calculate_pace(AVContentType, AVPage, AVPageData, AVPace)
        else:
            print "Pick avclub or onion dummy!"