"""
ASGI para o projeto CTI.

:created by:    Mateus Herrera
:created at:    2024-10-25
"""

import os

from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cti.settings')
application = get_asgi_application()
