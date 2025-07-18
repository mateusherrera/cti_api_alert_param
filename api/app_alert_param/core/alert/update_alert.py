"""
Módulo responsável por atualizar proximo dia a rodar alerta.

:created by:    Mateus Herrera
:created at:    2025-07-18
"""

import datetime

from rest_framework             import status
from rest_framework.request     import Request
from rest_framework.response    import Response

from app_alert_param.core.alert.create_alert import CreateAlert

from core.response_utils.response_builder    import ResponseBuilder
from core.response_utils.response_messages   import ResponseMessages
from core.response_utils.response_error_code import ResponseErrorCode

from app_alert_param.models         import Alert
from app_alert_param.serializers    import AlertSerializer


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

    @classmethod
    def list(cls, request: Request) -> Response:
        """
        Sobrescreve o método list para incluir campos adicionais nos relacionamentos ManyToMany.

        :param request: Requisição HTTP.
        :return:        Resposta HTTP contendo a lista de alertas com campos adicionais.
        """

        alerts = Alert.objects.all()

        try:
            data = cls.get_data_alert(request, alerts)

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
    
    @classmethod
    def list_by_user(cls, request: Request, user_id: int) -> Response:
        """
        Listar alerta de um usuário.

        :param request: Requisição HTTP.
        :param user_id: ID do usuário.
        :return:        Resposta HTTP contendo a lista de alertas com campos adicionais.
        """

        alerts = Alert.objects.filter(id_user=user_id)

        try:
            data = cls.get_data_alert(request, alerts)

        except Exception as err:
            return ResponseBuilder.build_response(
                ResponseMessages.ERROR_LIST_ALERTS,
                error={
                    'code': ResponseErrorCode.ERROR_LIST_ALERTS_BY_USER[0],
                    'message': ResponseErrorCode.ERROR_LIST_ALERTS_BY_USER[1],
                    'error': f'{type(err)}'
                },
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return ResponseBuilder.build_response(
            ResponseMessages.LIST_ALERTS,
            data=data
        )
    
    @classmethod
    def list_active_by_user(cls, request: Request, user_id: int) -> Response:
        """
        Listar alertas ativos de um usuário.

        :param request: Requisição HTTP.
        :param user_id: ID do usuário.
        :return:        Resposta HTTP contendo a lista de alertas ativos com campos adicionais.
        """

        active_alerts = Alert.objects.filter(id_user=user_id, is_active=True)

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
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return ResponseBuilder.build_response(
            ResponseMessages.LIST_ALERTS,
            data=data
        )
    
    @classmethod
    def list_active_alerts_run_today(cls, request: Request) -> Response:
        """
        Listar alertas ativos cujo campo 'run' é igual à data de hoje.

        :param request: Requisição HTTP.
        :return:        Resposta HTTP contendo a lista de alertas ativos com 'run' igual à data de hoje.
        """

        today = datetime.date.today()
        active_alerts = Alert.objects.filter(run=today, is_active=True)

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
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return ResponseBuilder.build_response(
            ResponseMessages.LIST_ALERTS,
            data=data
        )

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
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        serializer = AlertSerializer(alert, context={'request': request})

        data = serializer.data
        data = UpdateAlert.get_ntn_fields(alert, data)

        return ResponseBuilder.build_response(
            ResponseMessages.ALERT_RUN_UPDATED,
            data=data
        )

    @staticmethod
    def deactivate(request: Request, alert: Alert) -> Response:
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
    def update_keywords(request: Request, alert: Alert) -> Response:
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
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        serializer = AlertSerializer(alert, context={'request': request})

        data = serializer.data
        data = UpdateAlert.get_ntn_fields(alert, data)

        return ResponseBuilder.build_response(
            ResponseMessages.ALERT_KEYWORDS_UPDATED,
            data=data
        )
    
    @staticmethod
    def update_forums(request: Request, alert: Alert) -> Response:
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
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        serializer = AlertSerializer(alert, context={'request': request})

        data = serializer.data
        data = UpdateAlert.get_ntn_fields(alert, data)

        return ResponseBuilder.build_response(
            ResponseMessages.ALERT_FORUMS_UPDATED,
            data=data
        )
    
    @staticmethod
    def update_emails(request: Request, alert: Alert) -> Response:
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
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
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
