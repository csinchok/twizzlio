import os

from fabric.api import *
from fabric.contrib.project import rsync_project
from fabric.contrib import files

from contextlib import contextmanager as _contextmanager

env.hosts = ['66.175.213.211']
env.user = 'fabric'
env.webroot = '/www/'
env.projectroot = os.path.join(env.webroot, 'twizzlio')
env.activate = 'source .env/bin/activate'

@_contextmanager
def virtualenv():
    with cd(env.projectroot):
        with prefix(env.activate):
            yield

def deploy():
    rsync_project(env.webroot, delete=True, exclude=['.env', '*.db', '*.pyc', '.git', 'twizzlio/webroot/static', 'twizzlio/webroot/media'])
    with virtualenv():
        run('pip install -r requirements.txt')
        run('python manage.py collectstatic --noinput')
        run('DJANGO_SETTINGS_MODULE=twizzlio.production python manage.py syncdb --noinput')
        run('DJANGO_SETTINGS_MODULE=twizzlio.production python manage.py migrate')
        run('supervisorctl reload')