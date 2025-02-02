"""
Urls do projeto CTI.

:created by:    Mateus Herrera
:created at:    2024-10-25
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from alert_param.urls import alert_param_router


BASE    = 'api'
VERSION = 'v1'

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),

    # API de perfis de alerta
    path(f'{BASE}/{VERSION}/', include(alert_param_router.urls)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
