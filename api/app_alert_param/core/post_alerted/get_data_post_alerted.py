"""
Arquivo para implementação dos métodos para recuperar informações de post alertados.

:created by:    Mateus Herrera
:created at:    2025-07-18
"""

from rest_framework             import status
from rest_framework.request     import Request
from rest_framework.response    import Response

from core.response_utils.response_builder    import ResponseBuilder
from core.response_utils.response_messages   import ResponseMessages
from core.response_utils.response_error_code import ResponseErrorCode

from app_alert_param.models         import PostAlerted
from app_alert_param.serializers    import PostAlertedSerializer


class GetDataPostAlerted:
    """ Classe responsável por obter os dados de posts alertados. """

    # ini: methods

    @staticmethod
    def _get_data_post_alerted(request: Request, posts_alerted: PostAlerted) -> list:
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
    
    @classmethod
    def list(cls, request: Request) -> Response:
        """
        Método para listar os posts alertados.

        :param request: Requisição HTTP.
        :return:        Resposta HTTP contendo os posts alertados.
        """

        posts_alerted = PostAlerted.objects.all()

        try:
            data = cls._get_data_post_alerted(request, posts_alerted)

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
    
    @classmethod
    def list_by_alert(cls, request: Request, alert_id: int) -> Response:
        """
        Método para listar os posts alertados por um alerta específico.

        :param request:     Requisição HTTP.
        :param alert_id:    ID do alerta cujos posts alertados serão filtrados.
        :return:            Resposta HTTP contendo os posts alertados do alerta.
        """

        posts_alerted = PostAlerted.objects.filter(alert_id=alert_id)
        data = list()

        try:
            data = cls._get_data_post_alerted(request, posts_alerted)

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

    # end: methods
