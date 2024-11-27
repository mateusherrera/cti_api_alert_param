"""
Endpoints para app (alert_param).

:author:        Mateus Herrera Gobetti Borges
:github:        mateusherrera

:created at:    2024-09-25
:updated at:    2024-09-25
"""

from rest_framework.routers import SimpleRouter

from .views import (
    AlertViewSet,
    KeywordViewSet,
    ForumViewSet,
    EmailViewSet,
)


# Recursos
ALERTS = 'alerts'
KEYWORDS = 'keywords'
FORUMS = 'forums'
EMAILS = 'emails'

# Registra as views no roteador
alert_param_router = SimpleRouter()
alert_param_router.register(ALERTS, AlertViewSet)
alert_param_router.register(KEYWORDS, KeywordViewSet)
alert_param_router.register(FORUMS, ForumViewSet)
alert_param_router.register(EMAILS, EmailViewSet)
