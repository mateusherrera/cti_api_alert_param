from rest_framework.decorators import action
from rest_framework.response import Response
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

    @action(detail=True, methods=['get'], url_path='keywords')
    def get_keywords(self, request, pk=None):
        param = self.get_object()
        keywords = param.keywords.all()
        serializer = KeywordSerializer(keywords, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='emails')
    def get_emails(self, request, pk=None):
        param = self.get_object()
        emails = param.emails.all()
        serializer = EmailSerializer(emails, many=True)
        return Response(serializer.data)

    pass


class KeywordViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
    pass


class EmailViewSet(viewsets.ModelViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    pass
