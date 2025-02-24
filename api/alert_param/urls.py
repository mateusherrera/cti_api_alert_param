"""
Endpoints para app (alert_param).

:created by:    Mateus Herrera
:created at:    2024-10-25
"""

from rest_framework.routers import SimpleRouter

from alert_param.views import (
    AlertViewSet,
    ForumViewSet,
    EmailViewSet,
    KeywordViewSet,
    PostAlertedViewSet,
)


# Recursos
ALERTS       = 'alert'
FORUMS       = 'forum'
EMAILS       = 'email'
KEYWORDS     = 'keyword'
POST_ALERTED = 'post_alerted'

# Registra as views no roteador
alert_param_router = SimpleRouter()
alert_param_router.register( ALERTS         , AlertViewSet               )
alert_param_router.register( FORUMS         , ForumViewSet               )
alert_param_router.register( EMAILS         , EmailViewSet               )
alert_param_router.register( KEYWORDS       , KeywordViewSet             )
alert_param_router.register( POST_ALERTED   , PostAlertedViewSet         )
