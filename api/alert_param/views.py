"""
Módulo que define as views da aplicação alert_param.

:created by:    Mateus Herrera
:created at:    2024-10-25
"""

import datetime

from rest_framework             import status
from rest_framework             import viewsets
from rest_framework.decorators  import action
from rest_framework.response    import Response

from core.response_utils.response_builder    import ResponseBuilder
from core.response_utils.response_messages   import ResponseMessages
from core.response_utils.response_error_code import ResponseErrorCode

from alert_param.core.alert.create_alert                import CreateAlert
from alert_param.core.alert.update_alert                import UpdateAlert
from alert_param.core.post_alerted.create_post_alerted  import CreatePostAlerted

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

        try:
            alert = Alert.objects.get(pk=pk)
        except Alert.DoesNotExist as err:
            return ResponseBuilder.build_response(
                ResponseMessages.ERROR_FOUND_ALERT,
                error={
                    'code': ResponseErrorCode.ERROR_ALERT_UPDATE_RUN[0],
                    'message': ResponseErrorCode.ERROR_ALERT_UPDATE_RUN[1],
                    'error': f'{type(err)}'
                },
                http_status=status.HTTP_404_NOT_FOUND
            )
        return UpdateAlert().update_run(request, alert)

    @action(detail=True, methods=['put'], url_path='keywords')
    def update_keywords(self, request, pk=None):
        """
        Atualiza as palavras-chave de um alerta.

        :param request: Requisição HTTP.
        :param pk:      Chave primária do alerta.
        :return:        Resposta HTTP contendo o alerta atualizado.
        """

        try:
            alert = Alert.objects.get(pk=pk)
        except Alert.DoesNotExist as err:
            return ResponseBuilder.build_response(
                ResponseMessages.ERROR_FOUND_ALERT,
                error={
                    'code': ResponseErrorCode.ERROR_UPDATE_KEYWORDS[0],
                    'message': ResponseErrorCode.ERROR_UPDATE_KEYWORDS[1],
                    'error': f'{type(err)}'
                },
                http_status=status.HTTP_404_NOT_FOUND
            )

        return UpdateAlert().update_keywords(request, alert)
    
    @action(detail=True, methods=['put'], url_path='forums')
    def update_forums(self, request, pk=None):
        """
        Atualiza os fóruns de um alerta.

        :param request: Requisição HTTP.
        :param pk:      Chave primária do alerta.
        :return:        Resposta HTTP contendo o alerta atualizado.
        """

        try:
            alert = Alert.objects.get(pk=pk)
        except Alert.DoesNotExist as err:
            return ResponseBuilder.build_response(
                ResponseMessages.ERROR_FOUND_ALERT,
                error={
                    'code': ResponseErrorCode.ERROR_UPDATE_FORUMS[0],
                    'message': ResponseErrorCode.ERROR_UPDATE_FORUMS[1],
                    'error': f'{type(err)}'
                },
                http_status=status.HTTP_404_NOT_FOUND
            )

        return UpdateAlert().update_forums(request, alert)
    
    @action(detail=True, methods=['put'], url_path='emails')
    def update_emails(self, request, pk=None):
        """
        Atualiza os e-mails de um alerta.

        :param request: Requisição HTTP.
        :param pk:      Chave primária do alerta.
        :return:        Resposta HTTP contendo o alerta atualizado.
        """

        try:
            alert = Alert.objects.get(pk=pk)
        except Alert.DoesNotExist as err:
            return ResponseBuilder.build_response(
                ResponseMessages.ERROR_FOUND_ALERT,
                error={
                    'code': ResponseErrorCode.ERROR_UPDATE_EMAILS[0],
                    'message': ResponseErrorCode.ERROR_UPDATE_EMAILS[1],
                    'error': f'{type(err)}'
                },
                http_status=status.HTTP_404_NOT_FOUND
            )

        return UpdateAlert().update_emails(request, alert)

    @action(detail=True, methods=['get'], url_path='deactivate')
    def deactivate(self, request, pk=None):
        """
        Desativa um alerta.

        :param request: Requisição HTTP.
        :param pk:      Chave primária do alerta.
        :return:        Resposta HTTP contendo o alerta desativado.
        """

        try:
            alert = Alert.objects.get(pk=pk)
        except Alert.DoesNotExist as err:
            return ResponseBuilder.build_response(
                ResponseMessages.ERROR_FOUND_ALERT,
                error={
                    'code': ResponseErrorCode.ERROR_DEACTIVATE_ALERT[0],
                    'message': ResponseErrorCode.ERROR_DEACTIVATE_ALERT[1],
                    'error': f'{type(err)}'
                },
                http_status=status.HTTP_404_NOT_FOUND
            )

        return UpdateAlert().deactivate(request, alert)

    def list(self, request, *args, **kwargs):
        """
        Sobrescreve o método list para incluir campos adicionais nos relacionamentos ManyToMany.

        :param request: Requisição HTTP.
        :return:        Resposta HTTP contendo a lista de alertas com campos adicionais.
        """
        
        alerts = Alert.objects.all()
        data = list()

        try:
            data = UpdateAlert.get_data_alert(request, alerts)

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
        data = list()

        try:
            data = UpdateAlert.get_data_alert(request, alerts)

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
        data = list()

        try:
            data = UpdateAlert.get_data_alert(request, active_alerts)

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
        data = list()

        try:
            data = UpdateAlert.get_data_alert(request, active_alerts)

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

    def create(self, request, *args, **kwargs):
        """
        Cria um novo post alertado.

        :param request: Requisição HTTP.
        :return:        Resposta HTTP contendo o post alertado criado.
        """

        return CreatePostAlerted.create(request)
    
    @staticmethod
    def _get_data_post_alerted(request, posts_alerted):
        """
        Retorna os dados dos posts alertados.

        :param request:         Requisição HTTP.
        :param posts_alerted:   QuerySet contendo os posts alertados.
        :return:                Lista contendo os dados dos posts alertados.
        """

        data = list()

        for post_alerted in posts_alerted:
            post_alerted_data = PostAlertedSerializer(post_alerted, context={'request': request}).data
            post_alerted_data['keywords_found'] = [ keyword.word for keyword in post_alerted.keywords_found.all() ]
            post_alerted_data['forum'] = post_alerted.forum.forum_name
            data.append(post_alerted_data)

        return data

    def list(self, request, *args, **kwargs):
        """
        Sobrescreve o método list para incluir campos adicionais nos relacionamentos ManyToMany.

        :param request: Requisição HTTP.
        :return:        Resposta HTTP contendo a lista de posts alertados com campos adicionais.
        """

        posts_alerted = PostAlerted.objects.all()
        data = list()

        try:
            data = self._get_data_post_alerted(request, posts_alerted)

        except Exception as err:
            return ResponseBuilder.build_response(
                ResponseMessages.ERROR_LIST_POSTS_ALERTED,
                error={
                    'code': ResponseErrorCode.ERROR_LIST_POSTS_ALERTED[0],
                    'message': ResponseErrorCode.ERROR_LIST_POSTS_ALERTED[1],
                    'error': f'{type(err)}'
                },
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return ResponseBuilder.build_response(
            ResponseMessages.LIST_POSTS_ALERTED,
            data=data
        )
    
    @action(detail=False, methods=['get'], url_path='alert/(?P<id_alert>[^/.]+)')
    def get_post_alerted_by_alert(self, request, id_alert=None):
        """
        Retorna os posts alertados associados a um determinado alerta.

        :param request:     Requisição HTTP.
        :param id_alert:    ID do alerta cujos posts alertados serão filtrados.
        :return:            Resposta HTTP contendo os posts alertados do alerta.
        """

        posts_alerted = PostAlerted.objects.filter(alert_id=id_alert)
        data = list()

        try:
            data = self._get_data_post_alerted(request, posts_alerted)

        except Exception as err:
            return ResponseBuilder.build_response(
                ResponseMessages.ERROR_LIST_POSTS_ALERTED,
                error={
                    'code': ResponseErrorCode.ERROR_LIST_POSTS_ALERTED_BY_ALERT[0],
                    'message': ResponseErrorCode.ERROR_LIST_POSTS_ALERTED_BY_ALERT[1],
                    'error': f'{type(err)}'
                },
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return ResponseBuilder.build_response(
            ResponseMessages.LIST_POSTS_ALERTED,
            data=data
        )

    pass
