from rest_framework import serializers
from .models import (
    Param,
    Keyword,
    Email,
    ParamKeyword,
    ParamEmail
)


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = [
            'id',
            'keyword',
        ]
        pass
    pass


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = [
            'id',
            'email',
        ]
        pass
    pass

class ParamSerializer(serializers.ModelSerializer):
    keyword_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    email_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    keywords = KeywordSerializer(many=True, read_only=True)
    emails = EmailSerializer(many=True, read_only=True)

    class Meta:
        extra_kwargs = {
            'keywords': { 'read_only': True },
            'emails': { 'read_only': True },
            'keyword_ids': { 'write_only': True },
            'email_ids': { 'write_only': True },
        }

        model = Param
        fields = [
            'id',
            'status',
            'relevant',
            'source',
            'forum',
            'keywords',
            'emails',
            'keyword_ids',
            'email_ids',
        ]
        pass

    def create(self, validated_data):
        keyword_ids = validated_data.pop('keyword_ids', [])
        email_ids = validated_data.pop('email_ids', [])

        param = Param.objects.create(**validated_data)

        # Relaciona os Keywords existentes ao Param
        for keyword_id in keyword_ids:
            keyword = Keyword.objects.get(id=keyword_id)
            ParamKeyword.objects.get_or_create(param=param, keyword=keyword)

        # Relaciona os Emails existentes ao Param
        for email_id in email_ids:
            email = Email.objects.get(id=email_id)
            ParamEmail.objects.get_or_create(param=param, email=email)

        return param

    def update(self, instance, validated_data):
        keyword_ids = validated_data.pop('keyword_ids', [])
        email_ids = validated_data.pop('email_ids', [])

        # Atualiza os campos básicos do Param
        instance.status = validated_data.get('status', instance.status)
        instance.relevant = validated_data.get('relevant', instance.relevant)
        instance.source = validated_data.get('source', instance.source)
        instance.forum = validated_data.get('forum', instance.forum)
        instance.save()

        # Limpa as relações existentes com Keywords e Emails
        if len(keyword_ids) != 0:
            instance.keywords.clear()

            # Relacionar ou criar novos Keywords
            for keyword_id in keyword_ids:
                keyword, created = Keyword.objects.get_or_create(id=keyword_id)
                ParamKeyword.objects.get_or_create(param=instance, keyword=keyword)

        if len(email_ids) != 0:
            instance.emails.clear()

            # Relacionar ou criar novos Emails
            for email_id in email_ids:
                email, created = Email.objects.get_or_create(id=email_id)
                ParamEmail.objects.get_or_create(param=instance, email=email)

        return instance

    pass
