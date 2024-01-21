import os
import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
bind = "0.0.0.0:8000"
wsgi_app = "rn24_backend.wsgi:application"
enable_stdio_inheritance = True

if os.getenv("DJANGO_DEBUG", "").upper() in ("Y", "TRUE", "ON", "1"):
    loglevel = "debug"
    reload = True
    workers = 4
