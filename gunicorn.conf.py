import multiprocessing
import os

workers = multiprocessing.cpu_count() * 2 + 1
bind = "0.0.0.0:8000"
wsgi_app = "rn24.wsgi:application"
enable_stdio_inheritance = True
graceful_timeout = 900
timeout = 900

if os.getenv("DJANGO_DEBUG", "").upper() in ("Y", "TRUE", "ON", "1"):
    loglevel = "debug"
    reload = True
    workers = 4
