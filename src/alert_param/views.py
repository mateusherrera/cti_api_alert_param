"""
Módulo que define as views da aplicação alert_param.

:author: Mateus Herrera Gobetti Borges
:github: mateusherrera

:created at: 2024-09-25
:updated at: 2024-09-25
"""

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

from .serializers import (
    AlertSerializer,
    KeywordSerializer,
    ForumSerializer,
    EmailSerializer,
)

from .models import (
    Alert,
    Keyword,
    Forum,
    Email,
)


class KeywordViewSet(viewsets.ModelViewSet):
    """ ViewSet para o modelo Keyword. """

    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
    pass


class ForumViewSet(viewsets.ModelViewSet):
    """ ViewSet para o modelo Forum. """

    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    pass


class EmailViewSet(viewsets.ModelViewSet):
    """ ViewSet para o modelo Email. """

    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    pass


class AlertViewSet(viewsets.ModelViewSet):
    """ ViewSet para o modelo Alert. """

    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

    @action(detail=True, methods=['get'], url_path='keywords')
    def get_keywords(self, request, pk=None):
        """
        Retorna os keywords associados ao alerta.

        :param request: Requisição HTTP.
        :param pk: Chave primária do alerta.
        :return: Resposta HTTP contendo os keywords associados ao alerta.
        """

        alert = self.get_object()
        keywords = alert.keywords.all()
        serializer = KeywordSerializer(keywords, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='forums')
    def get_forums(self, request, pk=None):
        """
        Retorna os fóruns associados ao alerta.

        :param request: Requisição HTTP.
        :param pk: Chave primária do alerta.
        :return: Resposta HTTP contendo os fóruns associados ao alerta.
        """

        alert = self.get_object()
        forums = alert.forums.all()
        serializer = ForumSerializer(forums, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='emails')
    def get_emails(self, request, pk=None):
        """
        Retorna os emails associados ao alerta.

        :param request: Requisição HTTP.
        :param pk: Chave primária do alerta.
        :return: Resposta HTTP contendo os emails associados ao alerta.
        """

        alert = self.get_object()
        emails = alert.emails.all()
        serializer = EmailSerializer(emails, many=True)
        return Response(serializer.data)

    pass
