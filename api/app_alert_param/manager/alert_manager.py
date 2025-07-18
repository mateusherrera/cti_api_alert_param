"""
Orquestrador para endpoints relacionados ao viewset de Parametros de Alerta.

:created by:    Mateus Herrera
:created at:    2025-07-18
"""

from rest_framework.request     import Request
from rest_framework.response    import Response

from app_alert_param.core.alert.create_alert import CreateAlert
from app_alert_param.core.alert.update_alert import UpdateAlert

from app_alert_param.models import Alert


class AlertManager:
    """ Class para gerenciar os endpoints relacionados ao viewset de Parametros de Alerta. """

    # ini: methods

    @staticmethod
    def create(request: Request) -> Response:
        """ Método para criar um novo alerta. """

        return CreateAlert.create(request)
    
    @staticmethod
    def update_run(request: Request, alert: Alert) -> Response:
        """ Método para atualizar o campo 'run' do alerta para a próxima data com base na frequência. """

        return UpdateAlert.update_run(request, alert)
    
    @staticmethod
    def update_keywords(request: Request, alert: Alert) -> Response:
        """ Método para atualizar as palavras-chave de um alerta. """

        return UpdateAlert.update_keywords(request, alert)
    
    @staticmethod
    def update_forums(request: Request, alert: Alert) -> Response:
        """ Método para atualizar os fóruns de um alerta. """

        return UpdateAlert.update_forums(request, alert)
    
    @staticmethod
    def update_emails(request: Request, alert: Alert) -> Response:
        """ Método para atualizar os emails de um alerta. """

        return UpdateAlert.update_emails(request, alert)
    
    @staticmethod
    def deactivate(request: Request, alert: Alert) -> Response:
        """ Método para desativar um alerta. """

        return UpdateAlert.deactivate(request, alert)
    
    @staticmethod
    def list(request: Request) -> Response:
        """ Sobrescreve o método list para incluir campos adicionais nos relacionamentos ManyToMany. """

        return UpdateAlert.list(request)

    @staticmethod
    def list_by_user(request: Request, user_id: str) -> Response:
        """ Método para retornar os alertas associados a um determinado user_id. """

        return UpdateAlert.list_by_user(request, user_id)
    
    @staticmethod
    def list_active_by_user(request: Request, user_id: str) -> Response:
        """ Método para retornar os alertas ativos associados a um determinado user_id. """

        return UpdateAlert.list_active_by_user(request, user_id)
    
    @staticmethod
    def list_active_alerts_run_today(request: Request) -> Response:
        """ Método para retornar os alertas ativos cujo campo 'run' é igual à data de hoje. """

        return UpdateAlert.list_active_alerts_run_today(request)

    # end: methods
