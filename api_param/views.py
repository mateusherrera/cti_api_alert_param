from rest_framework import viewsets
from .serializers import (
    ParamSerializer,
    KeywordSerializer,
    EmailSerializer,
)
from .models import (
    Param,
    Keyword,
    Email,
)


class ParamViewSet(viewsets.ModelViewSet):
    queryset = Param.objects.all()
    serializer_class = ParamSerializer
    pass


class KeywordViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
    pass


class EmailViewSet(viewsets.ModelViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    pass
