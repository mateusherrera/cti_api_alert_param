"""
WSGI para o projeto cti.

:created by:    Mateus Herrera
:created at:    2024-10-25
"""

import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cti.settings')
application = get_wsgi_application()
