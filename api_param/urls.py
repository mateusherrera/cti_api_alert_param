from rest_framework.routers import SimpleRouter
from .views import (
    ParamViewSet,
    KeywordViewSet,
    EmailViewSet,
)


# Recursos
PARAMS = 'params'
KEYWORDS = 'keywords'
EMAILS = 'emails'

router = SimpleRouter()
router.register(PARAMS, ParamViewSet)
router.register(KEYWORDS, KeywordViewSet)
router.register(EMAILS, EmailViewSet)
