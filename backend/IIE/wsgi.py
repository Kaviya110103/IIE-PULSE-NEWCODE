"""
WSGI config for IIE project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import time

from django.core.wsgi import get_wsgi_application
from django.db import connections
from django.db.utils import OperationalError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IIE.settings')


def wait_for_database(attempts=10, delay=3):
    for attempt in range(attempts):
        try:
            connections['default'].cursor()
            return
        except OperationalError:
            if attempt == attempts - 1:
                raise
            time.sleep(delay)

wait_for_database()
application = get_wsgi_application()
