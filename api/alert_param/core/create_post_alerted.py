"""
Módulo para classe de criação de registro de post alertado.

:created by:    Mateus Herrera
:created at:    2025-02-10
"""

from datetime import datetime
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from alert_param.core.utils.response_builder import ResponseBuilder
from alert_param.core.utils.response_messages import ResponseMessages
from alert_param.core.utils.response_error_code import ResponseErrorCode

from alert_param.models import (
    Alert,
    Forum,
    Keyword,
    PostAlerted,
)


class CreatePostAlerted:
    """ Classe para criação de registro de alertas. """

    # ini: methods

    @staticmethod
    def add_keywords_founded(post_alerted: PostAlerted, keywords_found: list):
        """
        Adiciona palavras-chave encontradas no texto do post.

        :param post_alerted:    PostAlerted - Objeto do post alertado.
        :param keywords_found:  list - Lista de palavras-chave encontradas.
        """

        for keyword in keywords_found:
            try:
                keyword_obj = Keyword.objects.get(word=str(keyword).upper())
                post_alerted.keywords_found.add(keyword_obj)

            except:
                raise ValueError(f'Erro ao adicionar palavras-chave {keyword}.')
            
    @staticmethod
    def get_response_data(post_alerted: PostAlerted) -> dict:
        """
        Monta dados para retorno da resposta HTTP.

        :param post_alerted:    PostAlerted - Objeto do post alertado.
        :return:                dict - Dados para retorno da resposta HTTP.
        """

        return {
            'id'            : post_alerted.id,

            'alert'         : post_alerted.alert.id,
            'keywords_found': [ keyword.word for keyword in post_alerted.keywords_found.all() ],
            'forum'         : post_alerted.forum.forum_name,
            'relevance'     : post_alerted.relevance,

            'id_post'       : post_alerted.id_post,
            'title'         : post_alerted.title,
            'description'   : post_alerted.description,
            'date'          : post_alerted.date,
        }

    @staticmethod
    def create(request: Request) -> Response:
        """
        Método para criação de registro de alertas.

        :param request: Request - Requisição HTTP.
        :return:        Response - Resposta HTTP.
        """

        try:
            data = request.data

        except Exception as err:
            return ResponseBuilder.build_response(
                ResponseMessages.ERROR_EMPTY_BODY,

                error={
                    'code'      : ResponseErrorCode.ERROR_EMPTY_BODY[0],
                    'message'   : ResponseErrorCode.ERROR_EMPTY_BODY[1],
                    'request'   : request.data or None,
                    'error'     : f'{type(err)}',
                },
                http_status=status.HTTP_400_BAD_REQUEST
            )

        try:
            id_post         = data['id_post']
            title           = data['title']
            description     = data['description']
            alert           = Alert.objects.get(id=int(data['alert']))
            forum           = Forum.objects.get(forum_name=data['forum'].upper())

            keywords_found  = list(data['keywords_found'])

            relevance       = float(data['relevance'])
            date            = data['date']

        except KeyError as err:
            return ResponseBuilder.build_response(
                ResponseMessages.ERROR_MISSING_FIELDS,

                error={
                    'code'      : ResponseErrorCode.ERROR_MISSING_FIELDS[0],
                    'message'   : ResponseErrorCode.ERROR_MISSING_FIELDS[1],
                    'request'   : request.data or None,
                    'error'     : f'{type(err)}',
                },
                http_status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as err:
            return ResponseBuilder.build_response(
                ResponseMessages.ERROR_GET_REQUEST,

                error={
                    'code'      : ResponseErrorCode.ERROR_GET_REQUEST[0],
                    'message'   : ResponseErrorCode.ERROR_GET_REQUEST[1],
                    'request'   : request.data or None,
                    'error'     : f'{type(err)}',
                },
                http_status=status.HTTP_400_BAD_REQUEST
            )

        try:
            post_alerted = PostAlerted.objects.create(
                id_post=id_post,
                title=title,
                description=description,
                alert=alert,
                forum=forum,
                relevance=relevance,
                date=date
            )

            post_alerted.keywords_found.set([])

        except:
            return ResponseBuilder.build_response(
                ResponseMessages.ERROR_CREATE_POST_ALERTED,

                error={
                    'code'      : ResponseErrorCode.ERROR_CREATE_POST_ALERTED[0],
                    'message'   : ResponseErrorCode.ERROR_CREATE_POST_ALERTED[1],
                    'request'   : request.data or None,
                    'error'     : f'{type(err)} - {str(err)}',
                },
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            CreatePostAlerted.add_keywords_founded(post_alerted, keywords_found)

        except Exception as err:
            post_alerted.delete()

            return ResponseBuilder.build_response(
                ResponseMessages.ERROR_CREATE_POST_ALERTED,

                error={
                    'code'      : ResponseErrorCode.ERROR_ADD_KEYWORD[0],
                    'message'   : ResponseErrorCode.ERROR_ADD_KEYWORD[1],
                    'request'   : request.data or None,
                    'error'     : f'{type(err)}',
                },
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return ResponseBuilder.build_response(
            ResponseMessages.SUCCESS_CREATE_POST_ALERTED,

            data=CreatePostAlerted.get_response_data(post_alerted),
            http_status=status.HTTP_201_CREATED
        )

    # end: methods
