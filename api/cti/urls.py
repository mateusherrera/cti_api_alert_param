"""
URL configuration for cti project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from django.contrib import admin

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from alert_param.urls import alert_param_router


# URI BASE
BASE = 'api'
VERSION = 'v2'

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),

    # V2 API de perfis de alerta
    path(f'{BASE}/{VERSION}/', include(alert_param_router.urls)),

    # Simple JWT
    path(f'{BASE}/{VERSION}/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(f'{BASE}/{VERSION}/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
