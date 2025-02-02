"""
Models para parametrização de alertas gerados no sistema de identificação de incidentes de cibersegurança (cti).

:created by:    Mateus Herrera
:created at:    2024-10-25
"""

from django.db import models


class Base(models.Model):
    """ Model base para os modelos do aplicativo alert_param. """

    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """ Meta informações para a classe Base. """

        abstract = True

        pass

    pass


class Keyword(Base):
    """ Model para armazenar palavras-chave para busca de alertas. """

    word = models.CharField(max_length=100, unique=True)

    class Meta:
        """ Meta informações para a classe Keyword. """

        db_table = 'keyword'

        verbose_name = 'Keyword'
        verbose_name_plural = 'Keywords'

        pass

    def __str__(self):
        """
        Retorna uma representação em string do objeto Keyword.

        :return: Representação em string do objeto Keyword.
        """

        return f'ID: {self.id} - Palavra-chave: {self.word}'

    pass


class Forum(Base):
    """ Model para armazenar fóruns de discussão para busca de alertas. """

    forum_name = models.CharField(max_length=100, unique=True)

    class Meta:
        """ Meta informações para a classe Forum. """

        db_table = 'forum'

        verbose_name = 'Forum'
        verbose_name_plural = 'Forums'

        pass

    def __str__(self):
        """
        Retorna uma representação em string do objeto Forum.

        :return: Representação em string do objeto Forum.
        """

        return f'ID: {self.id} - Nome do Forum: {self.forum_name}'

    pass


class Email(Base):
    """ Model para armazenar emails para envio de alertas. """

    email = models.EmailField(unique=True)

    class Meta:
        """ Meta informações para a classe Email. """

        db_table = 'email'

        verbose_name = 'Email'
        verbose_name_plural = 'Emails'

        pass

    def __str__(self):
        """
        Retorna uma representação em string do objeto Email.

        :return: Representação em string do objeto Email.
        """

        return f'ID: {self.id} - Email: {self.email}'

    pass


class Alert(Base):
    """ Model para armazenar parâmetros de perfis de alertas criados. """

    # Columns
    is_active = models.BooleanField(default=True)
    id_user = models.IntegerField()
    start_date = models.DateField()
    final_date = models.DateField()
    qte_frequency = models.IntegerField()
    type_frequency = models.CharField(max_length=100)
    is_relevant = models.FloatField(default=1.0)
    last_run = models.DateField(null=True, blank=True)
    run = models.DateField(null=True, blank=True)

    # Relationships
    keywords = models.ManyToManyField('Keyword')
    forums = models.ManyToManyField('Forum')
    emails = models.ManyToManyField('Email')

    class Meta:
        """ Meta informações para a classe Alert. """

        db_table = 'alert'

        verbose_name = 'Alert'
        verbose_name_plural = 'Alerts'

        pass

    def __str__(self):
        """
        Retorna uma representação em string do objeto Alert.

        :return: Representação em string do objeto Alert.
        """

        return f'Perfil de alerta criado pelo usuário com identificador: {self.id_user}'
    
    def save(self, *args, **kwargs):
        """ Setar run com o mesmo valor de start_date. """

        if not self.run:
            self.run = self.start_date
        super().save(*args, **kwargs)

    pass
