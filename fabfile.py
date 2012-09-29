import os

from fabric.api import *
from fabric.contrib.project import rsync_project
from fabric.contrib import files

from contextlib import contextmanager as _contextmanager

env.hosts = ['66.175.213.211']
env.user = 'fabric'
env.webroot = '/www/'
env.projectroot = os.path.join(env.webroot, 'twizzlio')
env.activate = 'source bin/activate'

@_contextmanager
def virtualenv():
    with cd(env.projectroot):
        with prefix(env.activate):
            yield

def deploy():
    rsync_project(env.webroot, delete=True, exclude=['lib', 'bin', 'include', 'lib', '*.db', '*.pyc', '.git', 'webroot/static', 'twizzlio/webroot/media'])
    with virtualenv():
        run('pip install -r requirements.txt')
        run('DJANGO_SETTINGS_MODULE=production python manage.py collectstatic --noinput')
        run('DJANGO_SETTINGS_MODULE=production python manage.py syncdb --noinput')
        run('DJANGO_SETTINGS_MODULE=production python manage.py migrate')
        run('supervisorctl reload')
        run('supervisord')