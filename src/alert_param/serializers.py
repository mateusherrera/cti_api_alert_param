"""
Módulo que contém os serializadores dos models do app alert_param.

:author: Mateus Herrera Gobetti Borges
:github: mateusherrera

:created at: 2024-09-25
:updated at: 2024-09-25
"""

from rest_framework import serializers

from .models import (
    Alert,
    Keyword,
    Forum,
    Email,
)


class KeywordSerializer(serializers.ModelSerializer):
    """ Serializer para o model Keyword. """

    class Meta:
        """ Meta opções do serializer. """

        model = Keyword
        fields = (
            'id',
            'keyword',
        )

        pass

    pass


class ForumSerializer(serializers.ModelSerializer):
    """ Serializer para o model Forum. """

    class Meta:
        """ Meta opções do serializer. """

        model = Forum
        fields = (
            'id',
            'forum_name',
        )

        pass

    pass


class EmailSerializer(serializers.ModelSerializer):
    """ Serializer para o model Email. """

    class Meta:
        """ Meta opções do serializer. """

        model = Email
        fields = (
            'id',
            'email',
        )

        pass

    pass


class AlertSerializer(serializers.ModelSerializer):
    """ Serializer para o model Alert. """

    # POST para relacionamentos
    keyword_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    forum_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    email_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=True
    )

    # GET dos relacionamentos
    keywords = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='keyword-detail'
    )

    forums = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='forum-detail'
    )

    emails = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='email-detail'
    )

    class Meta:
        """ Meta opções do serializer. """

        model = Alert
        fields = (
            'id',
            'is_active',
            'id_user',
            'start_date',
            'final_date',
            'qte_frequency',
            'type_frequency',
            'is_relevant',

            # ini: elacionamentos
            'keywords',
            'keyword_ids',
            'forums',
            'forum_ids',
            'emails',
            'email_ids',
            # end: relacionamentos

            'run'
        )

        extra_kwargs = {
            'keywords': { 'read_only': True },
            'forums': { 'read_only': True },
            'emails': { 'read_only': True },

            'keyword_ids': { 'write_only': True },
            'forum_ids': { 'write_only': True },
            'email_ids': { 'write_only': True },
        }

        pass

    def validate_is_relevant(self, value):
        """
        Valida se o campo is_relevant é um número entre 0 e 1.

        :param value: Valor do campo is_relevant.
        :return: Valor validado.
        """

        if not (0 <= value <= 1):
            raise serializers.ValidationError("O campo 'is_relevant' deve ser um número entre 0 e 1.")

        value = value if value != 0 else 1.0
        return value

    def create(self, validated_data):
        """
        Validar criação de perfil de alerta.

        :param validated_data: Dados pré-validados.
        :return: Alert criado.
        """

        # Extrai os IDs dos relacionamentos Many-to-Many
        keyword_ids = validated_data.pop('keyword_ids', [])
        forum_ids = validated_data.pop('forum_ids', [])
        email_ids = validated_data.pop('email_ids', [])

        # Cria o Alert normalmente
        alert = Alert.objects.create(**validated_data)

        # Relaciona os Keywords, Forums e Emails diretamente ao Alert
        alert.keywords.set(keyword_ids)
        alert.forums.set(forum_ids)
        alert.emails.set(email_ids)

        return alert

    def update(self, instance, validated_data):
        """
        Validar atualização de perfil de alerta.

        :param instance: Instância do Alert.
        :param validated_data: Dados pré-validados.
        :return: Alert atualizado.
        """

         # Extrai os IDs dos relacionamentos Many-to-Many
        keyword_ids = validated_data.pop('keyword_ids', [])
        forum_ids = validated_data.pop('forum_ids', [])
        email_ids = validated_data.pop('email_ids', [])

        # Atualiza os campos normais do Alert
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.id_user = validated_data.get('id_user', instance.id_user)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.final_date = validated_data.get('final_date', instance.final_date)
        instance.qte_frequency = validated_data.get('qte_frequency', instance.qte_frequency)
        instance.type_frequency = validated_data.get('type_frequency', instance.type_frequency) 
        instance.is_relevant = validated_data.get('is_relevant', instance.is_relevant)
        instance.run = validated_data.get('run', instance.run)
        instance.save()

        # Atualiza as relações Many-to-Many, se fornecidas
        if keyword_ids:
            instance.keywords.set(keyword_ids)

        if forum_ids:
            instance.forums.set(forum_ids)

        if email_ids:
            instance.emails.set(email_ids)

        return instance

    pass
