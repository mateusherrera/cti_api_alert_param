"""
Endpoints para app (app_alert_param).

:created by:    Mateus Herrera
:created at:    2025-07-18
"""

from rest_framework.routers import SimpleRouter

from app_alert_param.views import (
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
app_alert_param_router = SimpleRouter()

# Registra os recursos no roteador
app_alert_param_router.register( ALERTS         , AlertViewSet               )
app_alert_param_router.register( FORUMS         , ForumViewSet               )
app_alert_param_router.register( EMAILS         , EmailViewSet               )
app_alert_param_router.register( KEYWORDS       , KeywordViewSet             )
app_alert_param_router.register( POST_ALERTED   , PostAlertedViewSet         )
