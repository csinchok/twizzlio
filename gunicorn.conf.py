import multiprocessing

bind = "unix:/tmp/gunicorn_twizzlio.sock"
workers = multiprocessing.cpu_count()