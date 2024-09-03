from rest_framework import serializers
from .models import (
    Param,
    Keyword,
    Email,
    Source,
    ParamKeyword,
    ParamEmail,
    ParamSource,
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


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = [
            'id',
            'name',
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
    source_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
    )

    keywords = KeywordSerializer(many=True, read_only=True)
    emails = EmailSerializer(many=True, read_only=True)
    sources = SourceSerializer(many=True, read_only=True)

    class Meta:
        extra_kwargs = {
            'keywords': { 'read_only': True },
            'emails': { 'read_only': True },
            'sources': { 'read_only': True },

            'keyword_ids': { 'write_only': True },
            'email_ids': { 'write_only': True },
            'source_ids': { 'write_only': True },
        }

        model = Param
        fields = [
            'id',
            'status',
            'is_relevant',
            'search_keyword',
            'search_source',
            'keywords',
            'emails',
            'sources',
            'keyword_ids',
            'email_ids',
            'source_ids',
        ]
        pass

    def create(self, validated_data):
        keyword_ids = validated_data.pop('keyword_ids', [])
        email_ids = validated_data.pop('email_ids', [])
        source_ids = validated_data.pop('source_ids', [])

        param = Param.objects.create(**validated_data)

        # Relaciona os Keywords existentes ao Param
        for keyword_id in keyword_ids:
            keyword = Keyword.objects.get(id=keyword_id)
            ParamKeyword.objects.get_or_create(param=param, keyword=keyword)

        # Relaciona os Emails existentes ao Param
        for email_id in email_ids:
            email = Email.objects.get(id=email_id)
            ParamEmail.objects.get_or_create(param=param, email=email)

        # Relaciona as Sources existentes ao Param
        for source_id in source_ids:
            source = Source.objects.get(id=source_id)
            ParamSource.objects.get_or_create(param=param, source=source)

        return param

    def update(self, instance, validated_data):
        keyword_ids = validated_data.pop('keyword_ids', [])
        email_ids = validated_data.pop('email_ids', [])
        source_ids = validated_data.pop('source_ids', [])

        # Atualiza os campos básicos do Param
        instance.status = validated_data.get('status', instance.status)
        instance.relevant = validated_data.get('is_relevant', instance.is_relevant)
        instance.forum = validated_data.get('search_keyword', instance.search_keyword)
        instance.source = validated_data.get('search_source', instance.search_source)
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

        if len(source_ids) != 0:
            instance.sources.clear()

            # Relacionar ou criar novas Sources
            for source_id in source_ids:
                source, created = Source.objects.get_or_create(id=source_id)
                ParamSource.objects.get_or_create(param=instance, source=source)

        return instance

    pass
