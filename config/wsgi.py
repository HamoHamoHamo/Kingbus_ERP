"""
WSGI config for ERP project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

# # 초기설정
# import os
# import sys

# sys.path.append('/home/tls1404/kingbus/Kingbus_ERP')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'ERP.settings'

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ERP.settings')

# application = get_wsgi_application()



import os, sys

from django.core.wsgi import get_wsgi_application
from config.settings.base import SERVER_ENV

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kenaf.settings')

# application = get_wsgi_application()

path = os.path.abspath(__file__ + "/../..")
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", SERVER_ENV)
application = get_wsgi_application()
