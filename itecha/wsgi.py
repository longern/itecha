"""
WSGI config for itecha project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itecha.settings')

application = get_wsgi_application()

def lambda_handler(event, context):
    from apig_wsgi import make_lambda_handler

    return make_lambda_handler(application)(event, context)
