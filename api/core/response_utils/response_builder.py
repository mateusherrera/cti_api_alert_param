"""
Esse módulo é responsável por construir as respostas das requisições da API.

:created by:        Mateus Herrera
:created at:        2025-02-02
"""

from rest_framework             import status
from rest_framework.response    import Response


class ResponseBuilder:
    """ Classe para construir as respostas das requisições da API. """

    @staticmethod
    def build_response(message: str, data=None, error=None, http_status=status.HTTP_200_OK) -> Response:
        """
        Método para construir a resposta da requisição.

        :param message: Mensagem da resposta.
        :param data: Dados da resposta.
        :param error: Erro da resposta.
        :param http_status: Status HTTP da resposta.
        :return: Dicionário com os dados da resposta.
        """

        if error:
            return Response(
                {
                    'message': message,
                    'error': error,
                },
                status=http_status
            )
        
        elif data:
            return Response(
                {
                    'message': message,
                    'data': data,
                },
                status=http_status
            )
        
        else:
            return Response(
                {
                    'message': message,
                },
                status=http_status
            )

    pass
