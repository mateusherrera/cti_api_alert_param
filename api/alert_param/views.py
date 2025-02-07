"""
Módulo que define as views da aplicação alert_param.

TODO: Melhorar retornos de metodos de alertas

:created by:    Mateus Herrera
:created at:    2024-10-25
"""

import datetime

from django.utils import timezone
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

    def list(self, request, *args, **kwargs):
        """
        Sobrescreve o método list para incluir campos adicionais nos relacionamentos ManyToMany.

        :param request: Requisição HTTP.
        :return:        Resposta HTTP contendo a lista de alertas com campos adicionais.
        """
        
        alerts = Alert.objects.all()
        data = []
        for alert in alerts:
            alert_data = AlertSerializer(alert, context={'request': request}).data
            alert_data['keywords'] = [keyword.word for keyword in alert.keywords.all()]
            alert_data['forums'] = [forum.forum_name for forum in alert.forums.all()]
            alert_data['emails'] = [email.email for email in alert.emails.all()]
            data.append(alert_data)
        return Response(data)

    @action(detail=True, methods=['get'], url_path='update/run')
    def update_run(self, request, pk=None):
        """
        Atualiza o campo 'run' do alerta para a próxima data com base na frequência.

        :param request: Requisição HTTP.
        :param pk:      Chave primária do alerta.
        :return:        Resposta HTTP contendo o alerta atualizado.
        """
        alert = self.get_object()

        last_run    = alert.run
        final_date  = alert.final_date

        if last_run >= final_date:
            alert.is_active = False
            alert.save()

            serializer = AlertSerializer(alert, context={'request': request})
            return Response(serializer.data)

        next_run = alert.run
        qte_frequency = alert.qte_frequency
        type_frequency = alert.type_frequency

        if type_frequency == 'days':
            next_run += datetime.timedelta(days=qte_frequency)
        elif type_frequency == 'weeks':
            next_run += datetime.timedelta(weeks=qte_frequency)
        elif type_frequency == 'months':
            next_run += datetime.timedelta(months=qte_frequency)
        elif type_frequency == 'years':
            next_run += datetime.timedelta(years=qte_frequency)

        if next_run > final_date:
            next_run = final_date

        alert.last_run = last_run
        alert.run = next_run
        alert.save()

        serializer = AlertSerializer(alert, context={'request': request})
        return Response(serializer.data)

    pass

    @action(detail=False, methods=['get'], url_path='user/(?P<id_user>[^/.]+)')
    def get_alerts_by_user(self, request, id_user=None):
        """
        Retorna os alertas associados a um determinado id_user.

        :param request: Requisição HTTP.
        :param id_user: ID do usuário cujos alertas serão filtrados.
        :return:        Resposta HTTP contendo os alertas do usuário.
        """

        alerts = Alert.objects.filter(id_user=id_user)
        
        data = []
        for alert in alerts:
            alert_data = AlertSerializer(alert, context={'request': request}).data
            alert_data['keywords'] = [keyword.word for keyword in alert.keywords.all()]
            alert_data['forums'] = [forum.forum_name for forum in alert.forums.all()]
            alert_data['emails'] = [email.email for email in alert.emails.all()]
            data.append(alert_data)
        
        return Response(data)

    @action(detail=False, methods=['get'], url_path='active/user/(?P<id_user>[^/.]+)')
    def get_active_alerts_by_user(self, request, id_user=None):
        """
        Retorna os alertas ativos associados a um determinado id_user.

        :param request: Requisição HTTP.
        :param id_user: ID do usuário cujos alertas ativos serão filtrados.
        :return:        Resposta HTTP contendo os alertas ativos do usuário.
        """

        active_alerts = Alert.objects.filter(id_user=id_user, is_active=True)
        
        data = []
        for alert in active_alerts:
            alert_data = AlertSerializer(alert, context={'request': request}).data
            alert_data['keywords'] = [keyword.word for keyword in alert.keywords.all()]
            alert_data['forums'] = [forum.forum_name for forum in alert.forums.all()]
            alert_data['emails'] = [email.email for email in alert.emails.all()]
            data.append(alert_data)
        
        return Response(data)

    @action(detail=False, methods=['get'], url_path='run/today')
    def get_active_alerts_run_today(self, request):
        """
        Retorna os alertas ativos cujo campo 'run' é igual à data de hoje.

        :param request: Requisição HTTP.
        :return:        Resposta HTTP contendo os alertas ativos com 'run' igual à data de hoje.
        """

        today = datetime.date.today()
        active_alerts = Alert.objects.filter(run=today, is_active=True)
        
        data = []
        for alert in active_alerts:
            alert_data = AlertSerializer(alert, context={'request': request}).data
            alert_data['keywords'] = [keyword.word for keyword in alert.keywords.all()]
            alert_data['forums'] = [forum.forum_name for forum in alert.forums.all()]
            alert_data['emails'] = [email.email for email in alert.emails.all()]
            data.append(alert_data)
        
        return Response(data)


class PostAlertedViewSet(viewsets.ModelViewSet):
    """ ViewSet para o modelo PostAlerted. """

    queryset = PostAlerted.objects.all()
    serializer_class = PostAlertedSerializer
    pass
