from rest_framework.routers import SimpleRouter

from .views import (
    ParamViewSet,
    KeywordViewSet,
    EmailViewSet,
    SourceViewSet,
)


# Recursos
PARAMS = 'params'
KEYWORDS = 'keywords'
EMAILS = 'emails'
SOURCES = 'sources'

router = SimpleRouter()
router.register(PARAMS, ParamViewSet)
router.register(KEYWORDS, KeywordViewSet)
router.register(EMAILS, EmailViewSet)
router.register(SOURCES, SourceViewSet)
