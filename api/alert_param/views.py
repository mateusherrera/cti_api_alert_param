"""
Módulo que define as views da aplicação alert_param.

    TODO: Alterar retornos para se adequar aos response_builders.

:created by:    Mateus Herrera
:created at:    2024-10-25
"""

from datetime import date
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from alert_param.core.create_alert import CreateAlert
from alert_param.serializers import (
    AlertSerializer,
    ForumSerializer,
    EmailSerializer,
    KeywordSerializer,
    PostAlertedSerializer,
)
from alert_param.models import (
    Alert,
    Forum,
    Email,
    Keyword,
    PostAlerted,
)


class KeywordViewSet(viewsets.ModelViewSet):
    """ ViewSet para o modelo Keyword. """

    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer

    def perform_create(self, serializer):
        """ Sobrescreve o método perform_create para garantir que o campo 'word' esteja em maiúsculo. """

        serializer.validated_data['word'] = serializer.validated_data['word'].upper()
        serializer.save()
        pass


class ForumViewSet(viewsets.ModelViewSet):
    """ ViewSet para o modelo Forum. """

    queryset = Forum.objects.all()
    serializer_class = ForumSerializer

    def perform_create(self, serializer):
        """ Sobrescreve o método perform_create para garantir que o campo 'forum_name' esteja em maiúsculo. """

        serializer.validated_data['forum_name'] = serializer.validated_data['forum_name'].upper()
        serializer.save()
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

    def create(self, request, *args, **kwargs):
        """
        Cria um novo alerta.

        :param request: Requisição HTTP.
        :return:        Resposta HTTP contendo o alerta criado.
        """

        return CreateAlert().create(request)

    @action(detail=False, methods=['get'], url_path='active')
    def get_active_alerts(self, request):
        """
        Retorna os alertas que estão ativos.

        :param request: Requisição HTTP.
        :return:        Resposta HTTP contendo os alertas ativos.
        """

        active_alerts = Alert.objects.filter(is_active=True)
        serializer = AlertSerializer(
            active_alerts,
            many=True,
            context={ 'request': request }
        )

        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='user/(?P<id_user>[^/.]+)')
    def get_alerts_by_user(self, request, id_user=None):
        """
        Retorna os alertas associados a um determinado id_user.

        :param request: Requisição HTTP.
        :param id_user: ID do usuário cujos alertas serão filtrados.
        :return:        Resposta HTTP contendo os alertas do usuário.
        """

        alerts = Alert.objects.filter(id_user=id_user)
        serializer = AlertSerializer(
            alerts,
            many=True,
            context={ 'request': request }
        )

        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='active/user/(?P<id_user>[^/.]+)')
    def get_active_alerts_by_user(self, request, id_user=None):
        """
        Retorna os alertas ativos associados a um determinado id_user.

        :param request: Requisição HTTP.
        :param id_user: ID do usuário cujos alertas ativos serão filtrados.
        :return:        Resposta HTTP contendo os alertas ativos do usuário.
        """

        active_alerts = Alert.objects.filter(id_user=id_user, is_active=True)
        serializer = AlertSerializer(
            active_alerts,
            many=True,
            context={ 'request': request }
        )

        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='keywords')
    def get_keywords(self, request, pk=None):
        """
        Retorna os keywords associados ao alerta.

        :param request: Requisição HTTP.
        :param pk:      Chave primária do alerta.
        :return:        Resposta HTTP contendo os keywords associados ao alerta.
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
        :param pk:      Chave primária do alerta.
        :return:        Resposta HTTP contendo os fóruns associados ao alerta.
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
        :param pk:      Chave primária do alerta.
        :return:        Resposta HTTP contendo os emails associados ao alerta.
        """

        alert = self.get_object()
        emails = alert.emails.all()
        serializer = EmailSerializer(emails, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='run/today')
    def get_alerts_run_today(self, request):
        """
        Retorna os alertas cujo campo 'run' é igual à data de hoje.

        :param request: Requisição HTTP.
        :return:        Resposta HTTP contendo os alertas com 'run' igual à data de hoje.
        """

        today = date.today()
        alerts = Alert.objects.filter(run=today)
        serializer = AlertSerializer(
            alerts,
            many=True,
            context={ 'request': request }
        )

        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='run/today/active')
    def get_active_alerts_run_today(self, request):
        """
        Retorna os alertas ativos cujo campo 'run' é igual à data de hoje.

        :param request: Requisição HTTP.
        :return:        Resposta HTTP contendo os alertas ativos com 'run' igual à data de hoje.
        """

        today = date.today()
        active_alerts = Alert.objects.filter(run=today, is_active=True)
        serializer = AlertSerializer(
            active_alerts,
            many=True,
            context={ 'request': request }
        )

        return Response(serializer.data)

    pass


class PostAlertedViewSet(viewsets.ModelViewSet):
    """ ViewSet para o modelo PostAlerted. """

    queryset = PostAlerted.objects.all()
    serializer_class = PostAlertedSerializer
    pass
