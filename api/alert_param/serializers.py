"""
Módulo que contém os serializadores dos models do app alert_param.

:created by:    Mateus Herrera
:created at:    2024-10-25
"""

from rest_framework import serializers
from datetime import date, timedelta

from alert_param.models import (
    Alert,
    Forum,
    Email,
    Keyword,
)


class ForumSerializer(serializers.ModelSerializer):
    """ Serializer para o model Forum. """

    class Meta:
        """ Meta opções do serializer. """

        model = Forum
        fields = '__all__'
        pass

    pass


class EmailSerializer(serializers.ModelSerializer):
    """ Serializer para o model Email. """

    class Meta:
        """ Meta opções do serializer. """

        model = Email
        fields = '__all__'
        pass

    pass


class KeywordSerializer(serializers.ModelSerializer):
    """ Serializer para o model Keyword. """

    class Meta:
        """ Meta opções do serializer. """

        model = Keyword
        fields = '__all__'
        pass

    pass


class AlertSerializer(serializers.ModelSerializer):
    """ Serializer para o model Alert. """

    class Meta:
        """ Meta opções do serializer. """

        model = Alert
        fields = '__all__'
        pass

    pass
