"""
WSGI para o projeto cti.

:created by:    Mateus Herrera
:created at:    2025-07-18
"""

import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_cti.settings')
application = get_wsgi_application()
