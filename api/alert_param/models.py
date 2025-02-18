"""
Models para parametrização de alertas gerados no sistema de identificação de incidentes de cibersegurança (cti).

:created by:    Mateus Herrera
:created at:    2024-10-25
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


SCHEMA_NAME = 'alert_param"."'

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


class Keyword(Base):
    """ Model para armazenar palavras-chave para busca de alertas. """

    word = models.CharField(max_length=100, unique=True)

    class Meta:
        """ Meta informações para a classe Keyword. """

        db_table = f'{SCHEMA_NAME}keyword'

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

        db_table = f'{SCHEMA_NAME}forum'

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

        db_table = f'{SCHEMA_NAME}email'

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

    forums      = models.ManyToManyField(Forum)
    emails      = models.ManyToManyField(Email)
    keywords    = models.ManyToManyField(Keyword)

    is_active       = models.BooleanField(default=True)
    id_user         = models.IntegerField()
    start_date      = models.DateField()
    final_date      = models.DateField()
    qte_frequency   = models.IntegerField()
    type_frequency  = models.CharField(max_length=100)
    is_relevant     = models.FloatField(
        default=1.0,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(1.0)
        ]
    )
    last_run        = models.DateField()
    run             = models.DateField()

    class Meta:
        """ Meta informações para a classe Alert. """

        db_table = f'{SCHEMA_NAME}alert'

        verbose_name = 'Alert'
        verbose_name_plural = 'Alerts'

        pass

    def __str__(self):
        """
        Retorna uma representação em string do objeto Alert.

        :return: Representação em string do objeto Alert.
        """

        return f'Perfil de alerta criado pelo usuário com identificador: {self.id_user}'

    pass


class PostAlerted(Base):
    """ Model para armazenar alertas gerados pelo sistema. """

    id_post         = models.IntegerField()
    title           = models.CharField(max_length=100)
    description     = models.TextField()
    alert           = models.ForeignKey(Alert, on_delete=models.CASCADE)
    forum           = models.ForeignKey(Forum, on_delete=models.CASCADE)
    keywords_found  = models.ManyToManyField(Keyword)
    relevance       = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    date            = models.DateField()

    class Meta:
        """ Meta informações para a classe GeneratedAlert. """

        db_table = f'{SCHEMA_NAME}post_alerted'

        verbose_name = 'Post Alerted'
        verbose_name_plural = 'Posts Alerted'
        pass

    def __str__(self):
        """
        Retorna uma representação em string do objeto GeneratedAlert.

        :return: Representação em string do objeto GeneratedAlert.
        """

        return f'ID: {self.id} - Título: {self.title}'

    pass
