"""
Módulo responsável por atualizar proximo dia a rodar alerta.

:created by:    Mateus Herrera
:created at:    2025-02-07
"""

import datetime

from rest_framework             import status
from rest_framework.request     import Request
from rest_framework.response    import Response

from alert_param.core.alert.create_alert import CreateAlert

from core.response_utils.response_builder    import ResponseBuilder
from core.response_utils.response_messages   import ResponseMessages
from core.response_utils.response_error_code import ResponseErrorCode

from alert_param.models         import Alert
from alert_param.serializers    import AlertSerializer


class UpdateAlert:
    """ Classe responsável por atualizar proximo dia a rodar alerta. """

    # ini: methods

    @staticmethod
    def get_ntn_fields(alert: Alert, data: dict) -> dict:
        """
        Retorna os campos necessários para atualizar alerta.

        :param data:    Dados do alerta.
        :return:        Dados tratados do Alerta
        """

        data['emails']      = [ email.email for email in alert.emails.all()      ]
        data['keywords']    = [ keyword.word for keyword in alert.keywords.all() ]
        data['forums']      = [ forum.forum_name for forum in alert.forums.all() ]
        return data
    
    @staticmethod
    def get_data_alert(request: Request, alerts: list) -> list:
        """
        Retorna os campos necessários para atualizar alerta.

        :param request: Request da requisição.
        :param alerts:  Lista de alertas.
        :return:        Lista de alertas tratados.
        """

        data = list()
        for alert in alerts:
            alert_data = AlertSerializer(alert, context={'request': request}).data
            alert_data = UpdateAlert.get_ntn_fields(alert, alert_data)
            data.append(alert_data)
        return data

    @staticmethod
    def update_run(request: Request, alert: Alert) -> Response:
        """
        Atualiza proximo dia a rodar alerta.

        :param request: Request da requisição.
        :param alert:   Objeto a se atualizar.
        :return:        Response do resultado.
        """

        last_run    = alert.run
        final_date  = alert.final_date

        if last_run >= final_date:
            alert.is_active = False
            alert.last_run = last_run
            alert.save()

            serializer = AlertSerializer(alert, context={'request': request})

            data = serializer.data
            data = UpdateAlert.get_ntn_fields(alert, data)

            return ResponseBuilder.build_response(
                ResponseMessages.ALERT_INACTIVE,
                data=data
            )

        try:
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

        except Exception as err:
            return ResponseBuilder.build_response(
                ResponseMessages.ERROR_ALERT_UPDATE_RUN,
                error={
                    'code': ResponseErrorCode.ERROR_ALERT_UPDATE_RUN[0],
                    'message': ResponseErrorCode.ERROR_ALERT_UPDATE_RUN[1],
                    'error': f'{type(err)}'
                },
                http_status=status.HTTP_500_INTERNAL_SERVER
            )

        serializer = AlertSerializer(alert, context={'request': request})

        data = serializer.data
        data = UpdateAlert.get_ntn_fields(alert, data)

        return ResponseBuilder.build_response(
            ResponseMessages.ALERT_RUN_UPDATED,
            data=data
        )

    @staticmethod
    def deactivate(request, alert):
        """
        Desativa alerta.

        :param request: Request da requisição.
        :param alert:   Objeto a se desativar.
        :return:        Response do resultado.
        """

        alert.is_active = False
        alert.save()

        serializer = AlertSerializer(alert, context={'request': request})

        data = serializer.data
        data = UpdateAlert.get_ntn_fields(alert, data)

        return ResponseBuilder.build_response(
            ResponseMessages.ALERT_INACTIVE,
            data=data
        )

    @staticmethod
    def update_keywords(request, alert):
        """
        Atualiza palavras-chave do alerta.

        :param request: Request da requisição.
        :param alert:   Objeto a se atualizar.
        :return:        Response do resultado.
        """

        try:
            nw_keywords = request.data.get('keywords', [])
            alert.keywords.clear()

            CreateAlert.add_keywords(alert, nw_keywords)

        except Exception as err:
            return ResponseBuilder.build_response(
                ResponseMessages.ERROR_ALERT_UPDATE_KEYWORDS,
                error={
                    'code': ResponseErrorCode.ERROR_UPDATE_KEYWORDS[0],
                    'message': ResponseErrorCode.ERROR_UPDATE_KEYWORDS[1],
                    'error': f'{type(err)}'
                },
                http_status=status.HTTP_500_INTERNAL_SERVER
            )
        
        serializer = AlertSerializer(alert, context={'request': request})

        data = serializer.data
        data = UpdateAlert.get_ntn_fields(alert, data)

        return ResponseBuilder.build_response(
            ResponseMessages.ALERT_KEYWORDS_UPDATED,
            data=data
        )
    
    @staticmethod
    def update_forums(request, alert):
        """
        Atualiza fóruns do alerta.

        :param request: Request da requisição.
        :param alert:   Objeto a se atualizar.
        :return:        Response do resultado.
        """

        try:
            nw_forums = request.data.get('forums', [])
            alert.forums.clear()

            CreateAlert.add_forums(alert, nw_forums)

        except Exception as err:
            return ResponseBuilder.build_response(
                ResponseMessages.ERROR_ALERT_UPDATE_FORUMS,
                error={
                    'code': ResponseErrorCode.ERROR_UPDATE_FORUMS[0],
                    'message': ResponseErrorCode.ERROR_UPDATE_FORUMS[1],
                    'error': f'{type(err)}'
                },
                http_status=status.HTTP_500_INTERNAL_SERVER
            )

        serializer = AlertSerializer(alert, context={'request': request})

        data = serializer.data
        data = UpdateAlert.get_ntn_fields(alert, data)

        return ResponseBuilder.build_response(
            ResponseMessages.ALERT_FORUMS_UPDATED,
            data=data
        )
    
    @staticmethod
    def update_emails(request, alert):
        """
        Atualiza emails do alerta.

        :param request: Request da requisição.
        :param alert:   Objeto a se atualizar.
        :return:        Response do resultado.
        """

        try:
            nw_emails = request.data.get('emails', [])
            alert.emails.clear()

            CreateAlert.add_emails(alert, nw_emails)

        except Exception as err:
            return ResponseBuilder.build_response(
                ResponseMessages.ERROR_ALERT_UPDATE_EMAILS,
                error={
                    'code': ResponseErrorCode.ERROR_UPDATE_EMAILS[0],
                    'message': ResponseErrorCode.ERROR_UPDATE_EMAILS[1],
                    'error': f'{type(err)}'
                },
                http_status=status.HTTP_500_INTERNAL_SERVER
            )

        serializer = AlertSerializer(alert, context={'request': request})

        data = serializer.data
        data = UpdateAlert.get_ntn_fields(alert, data)

        return ResponseBuilder.build_response(
            ResponseMessages.ALERT_EMAILS_UPDATED,
            data=data
        )

    # end: methods

    # end: class
    pass
