"""
ASGI para o projeto CTI.

:created by:    Mateus Herrera
:created at:    2025-07-18
"""

import os

from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_cti.settings')
application = get_asgi_application()
