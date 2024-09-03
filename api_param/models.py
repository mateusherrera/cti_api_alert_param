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
    relevant = models.BooleanField(default=False)
    source = models.BooleanField(default=False)
    forum = models.BooleanField(default=False)
    keywords = models.ManyToManyField('Keyword', through='ParamKeyword')
    emails = models.ManyToManyField('Email', through='ParamEmail')

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
