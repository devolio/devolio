"""
WSGI config for devolio project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if not os.environ.get('HEROKU_RT'):
    # .env module
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "devolio.settings")

application = get_wsgi_application()
