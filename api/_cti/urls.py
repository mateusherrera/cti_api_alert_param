"""
Urls do projeto CTI.

:created by:    Mateus Herrera
:created at:    2025-07-18
"""

from django.conf                import settings
from django.contrib             import admin
from django.urls                import path, include
from django.conf.urls.static    import static

from app_alert_param.urls import app_alert_param_router


# URL base da API
BASE    = 'api'
VERSION = 'v1'


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),

    # API de perfis de alerta
    path(f'{BASE}/{VERSION}/', include(app_alert_param_router.urls)),
]

urlpatterns += static( settings.STATIC_URL  ,   document_root=settings.STATIC_ROOT )
urlpatterns += static( settings.MEDIA_URL   ,   document_root=settings.MEDIA_ROOT  )
