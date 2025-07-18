"""
Módulo para classe de criação de registro de alertas.

:created by:    Mateus Herrera
:created at:    2025-07-18
"""

import pytz

from rest_framework             import status
from rest_framework.request     import Request
from rest_framework.response    import Response
from django.utils               import timezone
from datetime                   import datetime, date

from core.response_utils.response_builder    import ResponseBuilder
from core.response_utils.response_messages   import ResponseMessages
from core.response_utils.response_error_code import ResponseErrorCode

from app_alert_param.models import (
    Alert,
    Forum,
    Email,
    Keyword,
)


class CreateAlert:
    """  Classe para criação de registro de alertas. """

    @staticmethod
    def add_forums(alert: Alert, forums: list):
        """
        Método para adicionar fóruns.

        :param alert:  Objeto de alerta.
        :param forums: Lista de fóruns.
        """

        for forum in forums:
            try:
                forum_obj, _ = Forum.objects.get_or_create(forum_name=forum.upper())
                alert.forums.add(forum_obj)
            except:
                raise ValueError(f'Erro ao adicionar fóruns. (forum={forum})')

    @staticmethod
    def add_emails(alert: Alert, emails: list):
        """
        Método para adicionar e-mails.

        :param alert:  Objeto de alerta.
        :param emails: Lista de e-mails.
        """

        for email in emails:
            try:
                email_obj, _ = Email.objects.get_or_create(email=email)
                alert.emails.add(email_obj)
            except:
                raise ValueError(f'Erro ao adicionar e-mails. (email={email})')

    @staticmethod
    def add_keywords(alert: Alert, keywords: list):
        """
        Método para adicionar palavras-chave.

        :param alert:  Objeto de alerta.
        :param keywords: Lista de palavras-chave.
        """

        for keyword in keywords:
            try:
                keyword_obj, _ = Keyword.objects.get_or_create(word=keyword.upper())
                alert.keywords.add(keyword_obj)
            except:
                raise ValueError(f'Erro ao adicionar palavras-chave. (keyword={keyword})')

    @staticmethod
    def create_alerts(
            name: str,
            id_user: int,
            start_date: date,
            final_date: date,
            qte_frequency: int,
            type_frequency: str,
            is_relevant: float
        ) -> Alert:
        """
        Método para criação de alertas.

        :param name:            Nome do alerta.
        :param id_user:         ID do usuário.
        :param start_date:      Data inicial.
        :param final_date:      Data final.
        :param qte_frequency:   Frequência de quantidade.
        :param type_frequency:  Tipo de frequência.
        :param is_relevant:     Relevância.
        :return:                Objeto criado de alerta.
        """

        sao_paulo_tz = pytz.timezone('America/Sao_Paulo')
        start_date = datetime.combine(start_date, datetime.min.time()).astimezone(sao_paulo_tz).date()
        last_run = timezone.now().astimezone(sao_paulo_tz).date()

        run = start_date
        if type_frequency == 'days':
            run += timezone.timedelta(days=qte_frequency)
        elif type_frequency == 'weeks':
            run += timezone.timedelta(weeks=qte_frequency)
        elif type_frequency == 'months':
            run += timezone.timedelta(months=qte_frequency)
        elif type_frequency == 'years':
            run += timezone.timedelta(years=qte_frequency)
        else:
            raise ValueError('Tipo de frequência inválido.')

        if run > final_date:
            raise ValueError('A primeira data de execução não pode ultrapassar a data final.')

        alert = Alert.objects.create(
            name            = name,
            is_active       = True,
            id_user         = id_user,
            start_date      = start_date,
            final_date      = final_date,
            qte_frequency   = qte_frequency,
            type_frequency  = type_frequency,
            is_relevant     = is_relevant,
            last_run        = last_run,
            run             = run,
        )

        alert.forums.set([])
        alert.emails.set([])
        alert.keywords.set([])

        return alert

    @staticmethod
    def get_response_data(alert: Alert) -> dict:
        """
        Método para criação de dados de resposta.

        :param alert:  Objeto de alerta.
        :return:        Dados de resposta.
        """

        return {
            'id'            : alert.id,

            'name'          : alert.name,
            'forums'        : [ forum.forum_name for forum in alert.forums.all()    ],
            'emails'        : [ email.email for email in alert.emails.all()         ],
            'keywords'      : [ keyword.word for keyword in alert.keywords.all()    ],

            'is_active'     : alert.is_active,
            'id_user'       : alert.id_user,
            'start_date'    : alert.start_date,
            'final_date'    : alert.final_date,
            'qte_frequency' : alert.qte_frequency,
            'type_frequency': alert.type_frequency,
            'is_relevant'   : alert.is_relevant,
            'last_run'      : alert.last_run,
            'run'           : alert.run,
        }

    @staticmethod
    def create(request: Request) -> Response:
        """
        Método para criação de registro de alertas.

        :param request: Requisição de criação de alerta.
        :return:        Resposta da requisição.
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
            name            = data['name']

            keywords        = list(data['keywords'])
            forums          = list(data['forums'])
            emails          = list(data['emails'])

            id_user         = int(data['id_user'])
            start_date      = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            final_date      = datetime.strptime(data['final_date'], '%Y-%m-%d').date()
            qte_frequency   = int(data['qte_frequency'])
            type_frequency  = data['type_frequency']
            is_relevant     = float(data['is_relevant'])

            if start_date > final_date:
                return ResponseBuilder.build_response(
                    ResponseMessages.ERROR_INVALID_DATE,

                    error={
                        'code'      : ResponseErrorCode.ERROR_START_DATE[0],
                        'message'   : ResponseErrorCode.ERROR_START_DATE[1],
                        'request'   : request.data or None,
                    },
                    http_status=status.HTTP_400_BAD_REQUEST
                )
            
            if start_date < timezone.now().astimezone(pytz.timezone('America/Sao_Paulo')).date():
                start_date = datetime.strptime(datetime.strftime(start_date, '%Y-%m-%d'), '%Y-%m-%d').date()

            if final_date < timezone.now().astimezone(pytz.timezone('America/Sao_Paulo')).date():
                return ResponseBuilder.build_response(
                    ResponseMessages.ERROR_INVALID_DATE,

                    error={
                        'code'      : ResponseErrorCode.ERROR_INVALID_DATE[0],
                        'message'   : ResponseErrorCode.ERROR_INVALID_DATE[1],
                        'request'   : request.data or None,
                    },
                    http_status=status.HTTP_400_BAD_REQUEST
                )

        except KeyError as err:
            return ResponseBuilder.build_response(
                ResponseMessages.ERROR_MISSING_FIELDS,

                error={
                    'code'      : ResponseErrorCode.ERROR_MISSING_FIELDS[0],
                    'message'   : ResponseErrorCode.ERROR_MISSING_FIELDS[1],
                    'request'   : request.data or None,
                    'missing'   : f'{err}',
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
            alert = CreateAlert.create_alerts(
                name            = name,
                id_user         = id_user,
                start_date      = start_date,
                final_date      = final_date,
                qte_frequency   = qte_frequency,
                type_frequency  = type_frequency,
                is_relevant     = is_relevant,
            )

        except Exception as err:
            return ResponseBuilder.build_response(
                ResponseMessages.ERROR_CREATE_ALERT,

                error={
                    'code'      : ResponseErrorCode.ERROR_CREATE_ALERT[0],
                    'message'   : ResponseErrorCode.ERROR_CREATE_ALERT[1],
                    'request'   : request.data or None,
                    'error'     : f'{type(err)} - {str(err)}',
                },
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            CreateAlert.add_keywords(alert, keywords)

        except Exception as err:
            alert.delete()

            return ResponseBuilder.build_response(
                ResponseMessages.ERROR_CREATE_ALERT,

                error={
                    'code'      : ResponseErrorCode.ERROR_ADD_KEYWORD[0],
                    'message'   : ResponseErrorCode.ERROR_ADD_KEYWORD[1],
                    'request'   : request.data or None,
                    'error'     : f'{type(err)}',
                },
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            CreateAlert.add_forums(alert, forums)

        except Exception as err:
            alert.delete()

            return ResponseBuilder.build_response(
                ResponseMessages.ERROR_CREATE_ALERT,

                error={
                    'code'      : ResponseErrorCode.ERROR_ADD_FORUM[0],
                    'message'   : ResponseErrorCode.ERROR_ADD_FORUM[1],
                    'request'   : request.data or None,
                    'error'     : f'{type(err)}',
                },
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            CreateAlert.add_emails(alert, emails)

        except Exception as err:
            alert.delete()

            return ResponseBuilder.build_response(
                ResponseMessages.ERROR_CREATE_ALERT,

                error={
                    'code'      : ResponseErrorCode.ERROR_ADD_EMAIL[0],
                    'message'   : ResponseErrorCode.ERROR_ADD_EMAIL[1],
                    'request'   : request.data or None,
                    'error'     : f'{type(err)}',
                },
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return ResponseBuilder.build_response(
            ResponseMessages.SUCCESS_CREATE_ALERT,

            data=CreateAlert.get_response_data(alert),
            http_status=status.HTTP_201_CREATED
        )
