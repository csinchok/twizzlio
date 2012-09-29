from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'twizzlio',
        'USER': 'twizzlio',
        'PASSWORD': 'twizzlibro',
        'HOST': 'localhost',
    }
}

DEBUG = True
TEMPLATE_DEBUG = DEBUG

CELERY_ALWAYS_EAGER = False
THUMBNAIL_DUMMY = False