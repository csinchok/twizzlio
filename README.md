# Twizzl.io setup

    > brew install libmemcached
	> brew install libpng
	> brew install libjpeg

    > git clone git@github.com:csinchok/twizzlio.git
    > cd twizzlio
    > virtualenv .
    > source bin/activate
  	> pip install -r requirements.txt
	> python manage.py syncdb
	> python manage.py migrate
    > python manage.py runserver