from django.db import models


class Base(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        pass

    pass


class Param(Base):
    status = models.BooleanField(default=True)
    is_relevant = models.FloatField(default=1.0)
    search_keyword = models.BooleanField(default=False)
    search_source = models.BooleanField(default=False)
    keywords = models.ManyToManyField('Keyword', through='ParamKeyword')
    emails = models.ManyToManyField('Email', through='ParamEmail')
    sources = models.ManyToManyField('Source', through='ParamSource')

    class Meta:
        db_table = 'param'

        verbose_name = 'Param'
        verbose_name_plural = 'Params'
        pass

    pass


class Keyword(Base):
    keyword = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'keyword'

        verbose_name = 'Keyword'
        verbose_name_plural = 'Keywords'
        pass

    pass


class Email(Base):
    email = models.EmailField(unique=True)

    class Meta:
        db_table = 'email'

        verbose_name = 'Email'
        verbose_name_plural = 'Emails'
        pass

    pass


class Source(Base):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'source'

        verbose_name = 'Source'
        verbose_name_plural = 'Sources'
        pass

    pass


class ParamKeyword(Base):
    param = models.ForeignKey(Param, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)

    class Meta:
        db_table = 'param_keyword'

        verbose_name = 'Param Keyword'
        verbose_name_plural = 'Params Keywords'
        pass

    pass


class ParamEmail(Base):
    param = models.ForeignKey(Param, on_delete=models.CASCADE)
    email = models.ForeignKey(Email, on_delete=models.CASCADE)

    class Meta:
        db_table = 'param_email'

        verbose_name = 'Param Email'
        verbose_name_plural = 'Params Emails'
        pass

    pass


class ParamSource(Base):
    param = models.ForeignKey(Param, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)

    class Meta:
        db_table = 'param_source'

        verbose_name = 'Param Source'
        verbose_name_plural = 'Params Sources'
        pass

    pass
