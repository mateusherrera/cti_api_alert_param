"""
Definição da classe de configuração da aplicação app_alert_param.

:created by:    Mateus Herrera
:created at:    2025-07-18
"""

from django.apps import AppConfig


class AppAlertParamConfig(AppConfig):
    """ Classe de configuração da aplicação app_alert_param. """

    default_auto_field  = 'django.db.models.BigAutoField'
    name                = 'app_alert_param'

    verbose_name        = 'Parâmetros de Alerta'
    verbose_name_plural = 'Parâmetros de Alerta'
