"""
Módulo base para os modelos do aplicativo alert_param.

:created by:    Mateus Herrera
:created at:    2025-02-24
"""

from django.db import models


class Base(models.Model):
    """ Model base para os modelos do aplicativo alert_param. """

    id          = models.AutoField(primary_key=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        """ Meta informações para a classe Base. """

        abstract = True
        pass

    pass