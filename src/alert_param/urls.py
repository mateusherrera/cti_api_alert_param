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
