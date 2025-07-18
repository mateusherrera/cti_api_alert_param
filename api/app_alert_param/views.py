"""
Módulo que define as views da aplicação app_alert_param.

:created by:    Mateus Herrera
:created at:    2025-07-18
"""

from rest_framework.decorators  import action
from rest_framework.request     import Request
from rest_framework             import viewsets
from rest_framework.response    import Response

from app_alert_param.serializers import (
    AlertSerializer,
    ForumSerializer,
    EmailSerializer,
    KeywordSerializer,
    PostAlertedSerializer,
)
from app_alert_param.models import (
    Alert,
    Forum,
    Email,
    Keyword,
    PostAlerted,
)

from app_alert_param.manager.alert_manager          import AlertManager
from app_alert_param.manager.post_alerted_manager   import PostAlertedManager


class KeywordViewSet(viewsets.ModelViewSet):
    """ ViewSet para o modelo Keyword. """

    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer

    def perform_create(self, serializer: KeywordSerializer):
        """ Sobrescreve o método perform_create para garantir que o campo 'word' esteja em maiúsculo. """

        serializer.validated_data['word'] = serializer.validated_data['word'].upper()
        serializer.save()


class ForumViewSet(viewsets.ModelViewSet):
    """ ViewSet para o modelo Forum. """

    queryset = Forum.objects.all()
    serializer_class = ForumSerializer

    def perform_create(self, serializer: ForumSerializer):
        """ Sobrescreve o método perform_create para garantir que o campo 'forum_name' esteja em maiúsculo. """

        serializer.validated_data['forum_name'] = serializer.validated_data['forum_name'].upper()
        serializer.save()


class EmailViewSet(viewsets.ModelViewSet):
    """ ViewSet para o modelo Email. """

    queryset = Email.objects.all()
    serializer_class = EmailSerializer


class AlertViewSet(viewsets.ModelViewSet):
    """ ViewSet para o modelo Alert. """

    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

    def create(self, request: Request, *args, **kwargs) -> Response:
        """ Cria um novo alerta. """

        return AlertManager.create(request)

    @action(detail=True, methods=['get'], url_path='update/run')
    def update_run(self, request: Request, pk=None, *args, **kwargs) -> Response:
        """ Atualiza o campo 'run' do alerta para a próxima data com base na frequência. """

        alert = self.get_object()
        return AlertManager.update_run(request, alert)

    @action(detail=True, methods=['put'], url_path='keywords')
    def update_keywords(self, request: Request, pk=None, *args, **kwargs) -> Response:
        """ Atualiza as palavras-chave de um alerta. """

        alert = self.get_object()
        return AlertManager.update_keywords(request, alert)

    @action(detail=True, methods=['put'], url_path='forums')
    def update_forums(self, request: Request, pk=None, *args, **kwargs) -> Response:
        """ Atualiza os fóruns de um alerta. """

        alert = self.get_object()
        return AlertManager.update_forums(request, alert)

    @action(detail=True, methods=['put'], url_path='emails')
    def update_emails(self, request: Request, pk=None, *args, **kwargs) -> Response:
        """ Atualiza os e-mails de um alerta. """

        alert = self.get_object()
        return AlertManager.update_emails(request, alert)

    @action(detail=True, methods=['get'], url_path='deactivate')
    def deactivate(self, request: Request, pk=None, *args, **kwargs) -> Response:
        """ Desativa um alerta. """

        alert = self.get_object()
        return AlertManager.deactivate(request, alert)

    def list(self, request: Request, *args, **kwargs) -> Response:
        """ Sobrescreve o método list para incluir campos adicionais nos relacionamentos ManyToMany. """

        return AlertManager.list(request)

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def list_by_user(self, request: Request, user_id=None, *args, **kwargs) -> Response:
        """ Retorna os alertas associados a um determinado user_id. """

        return AlertManager.list_by_user(request, user_id)

    @action(detail=False, methods=['get'], url_path='active/user/(?P<user_id>[^/.]+)')
    def list_active_by_user(self, request: Request, user_id=None, *args, **kwargs) -> Response:
        """ Retorna os alertas ativos associados a um determinado user_id. """

        return AlertManager.list_active_by_user(request, user_id)

    @action(detail=False, methods=['get'], url_path='run/today')
    def list_active_alerts_run_today(self, request: Request, *args, **kwargs) -> Response:
        """ Retorna os alertas ativos cujo campo 'run' é igual à data de hoje. """

        return AlertManager.list_active_alerts_run_today(request)


class PostAlertedViewSet(viewsets.ModelViewSet):
    """ ViewSet para o modelo PostAlerted. """

    queryset = PostAlerted.objects.all()
    serializer_class = PostAlertedSerializer

    def create(self, request: Request, *args, **kwargs) -> Response:
        """ Cria um novo post alertado. """

        return PostAlertedManager.create(request)

    def list(self, request: Request, *args, **kwargs) -> Response:
        """ Sobrescreve o método list para incluir campos adicionais nos relacionamentos ManyToMany. """

        return PostAlertedManager.list(request)

    @action(detail=False, methods=['get'], url_path='alert/(?P<alert_id>[^/.]+)')
    def list_by_alert(self, request: Request, alert_id=None, *args, **kwargs) -> Response:
        """ Retorna os posts alertados associados a um determinado alerta. """

        return PostAlertedManager.list_by_alert(request, alert_id)
