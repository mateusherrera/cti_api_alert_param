"""
Orquestrador para endpoints relacionados ao viewset de Posts Alertados.

:created by:    Mateus Herrera
:created at:    2025-07-18
"""

from rest_framework.request     import Request
from rest_framework.response    import Response

from app_alert_param.core.post_alerted.create_post_alerted      import CreatePostAlerted
from app_alert_param.core.post_alerted.get_data_post_alerted    import GetDataPostAlerted


class PostAlertedManager:
    """ Class para gerenciar os endpoints relacionados ao viewset de Posts Alertados. """

    # ini: methods

    @staticmethod
    def create(request: Request) -> Response:
        """ Método para criar um novo post alertado. """

        return CreatePostAlerted.create(request)
    
    @staticmethod
    def list(request: Request) -> Response:
        """ Método para listar os posts alertados. """

        return GetDataPostAlerted.list(request)
    
    @staticmethod
    def list_by_alert(request: Request, alert_id: int) -> Response:
        """ Método para listar os posts alertados associados a um determinado alerta. """

        return GetDataPostAlerted.list_by_alert(request, alert_id)

    # end: methods
