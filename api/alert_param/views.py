"""
Módulo que define as views da aplicação alert_param.

TODO: Melhorar retornos de metodos de alertas

:created by:    Mateus Herrera
:created at:    2024-10-25
"""

import datetime

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


from alert_param.core.utils.response_builder import ResponseBuilder
from alert_param.core.utils.response_messages import ResponseMessages
from alert_param.core.utils.response_error_code import ResponseErrorCode

from alert_param.core.update_alert import UpdateAlert
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

    @action(detail=True, methods=['get'], url_path='update/run')
    def update_run(self, request, pk=None):
        """
        Atualiza o campo 'run' do alerta para a próxima data com base na frequência.

        :param request: Requisição HTTP.
        :param pk:      Chave primária do alerta.
        :return:        Resposta HTTP contendo o alerta atualizado.
        """

        alert = Alert.objects.get(pk=pk)
        return UpdateAlert().update_run(request, alert)

    def list(self, request, *args, **kwargs):
        """
        Sobrescreve o método list para incluir campos adicionais nos relacionamentos ManyToMany.

        :param request: Requisição HTTP.
        :return:        Resposta HTTP contendo a lista de alertas com campos adicionais.
        """
        
        alerts = Alert.objects.all()
        data = []

        try:
            for alert in alerts:
                alert_data = AlertSerializer(alert, context={'request': request}).data
                alert_data = UpdateAlert.get_ntn_fields(alert, alert_data)
                data.append(alert_data)

        except Exception as err:
            return ResponseBuilder.build_response(
                ResponseMessages.ERROR_LIST_ALERTS,
                error={
                    'code': ResponseErrorCode.ERROR_LIST_ALERTS[0],
                    'message': ResponseErrorCode.ERROR_LIST_ALERTS[1],
                    'error': f'{type(err)}'
                },
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return ResponseBuilder.build_response(
            ResponseMessages.LIST_ALERTS,
            data=data
        )

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

        try:
            for alert in alerts:
                alert_data = AlertSerializer(alert, context={'request': request}).data
                alert_data = UpdateAlert.get_ntn_fields(alert, alert_data)
                data.append(alert_data)

        except Exception as err:
            return ResponseBuilder.build_response(
                ResponseMessages.ERROR_LIST_ALERTS,
                error={
                    'code': ResponseErrorCode.ERROR_LIST_ALERTS_BY_USER[0],
                    'message': ResponseErrorCode.ERROR_LIST_ALERTS_BY_USER[1],
                    'error': f'{type(err)}'
                },
                http_status=status.HTTP_500_INTERNAL_SERVER
            )

        return ResponseBuilder.build_response(
            ResponseMessages.LIST_ALERTS,
            data=data
        )

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

        try:
            for alert in active_alerts:
                alert_data = AlertSerializer(alert, context={'request': request}).data
                alert_data = UpdateAlert.get_ntn_fields(alert, alert_data)
                data.append(alert_data)

        except Exception as err:
            return ResponseBuilder.build_response(
                ResponseMessages.ERROR_LIST_ALERTS,
                error={
                    'code': ResponseErrorCode.ERROR_LIST_ACTIVE_ALERTS_BY_USER[0],
                    'message': ResponseErrorCode.ERROR_LIST_ACTIVE_ALERTS_BY_USER[1],
                    'error': f'{type(err)}'
                },
                http_status=status.HTTP_500_INTERNAL_SERVER
            )

        return ResponseBuilder.build_response(
            ResponseMessages.LIST_ALERTS,
            data=data
        )

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

        try:
            for alert in active_alerts:
                alert_data = AlertSerializer(alert, context={'request': request}).data
                alert_data = UpdateAlert.get_ntn_fields(alert, alert_data)
                data.append(alert_data)

        except Exception as err:
            return ResponseBuilder.build_response(
                ResponseMessages.ERROR_LIST_ALERTS,
                error={
                    'code': ResponseErrorCode.ERROR_LIST_RUN_TODAY[0],
                    'message': ResponseErrorCode.ERROR_LIST_RUN_TODAY[1],
                    'error': f'{type(err)}'
                },
                http_status=status.HTTP_500_INTERNAL_SERVER
            )

        return ResponseBuilder.build_response(
            ResponseMessages.LIST_ALERTS,
            data=data
        )

    pass


class PostAlertedViewSet(viewsets.ModelViewSet):
    """ ViewSet para o modelo PostAlerted. """

    queryset = PostAlerted.objects.all()
    serializer_class = PostAlertedSerializer
    pass
