"""
WSGI config for college_erp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from .mongo_setup import connect

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_erp.settings')

connect()

application = get_wsgi_application()
