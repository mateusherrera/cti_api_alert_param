"""
Definição da classe de configuração da aplicação alert_param.

:created by:    Mateus Herrera
:created at:    2024-10-25
"""

from django.apps import AppConfig


class AlertParamConfig(AppConfig):
    """ Classe de configuração da aplicação alert_param. """

    default_auto_field  = 'django.db.models.BigAutoField'
    name                = 'alert_param'

    verbose_name        = 'Parâmetros de Alerta'
    verbose_name_plural = 'Parâmetros de Alerta'
    pass
