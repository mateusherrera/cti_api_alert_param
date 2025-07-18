"""
Models para parametrização de alertas gerados no sistema de identificação de incidentes de cibersegurança (cti).

:created by:    Mateus Herrera
:created at:    2025-07-18
"""

from django.db              import models
from django.core.validators import MinValueValidator, MaxValueValidator

from core.model.base import Base


SCHEMA_NAME = 'alert_param"."'


class Keyword(Base):
    """ Model para armazenar palavras-chave para busca de alertas. """

    word = models.CharField(max_length=100, unique=True)

    class Meta:
        """ Meta informações para a classe Keyword. """

        db_table            = f'{SCHEMA_NAME}keyword'
        verbose_name        = 'Keyword'
        verbose_name_plural = 'Keywords'

    def __str__(self):
        return f'{self.word} ({self.id})'


class Forum(Base):
    """ Model para armazenar fóruns de discussão para busca de alertas. """

    forum_name = models.CharField(max_length=100, unique=True)

    class Meta:
        """ Meta informações para a classe Forum. """

        db_table            = f'{SCHEMA_NAME}forum'
        verbose_name        = 'Forum'
        verbose_name_plural = 'Forums'

    def __str__(self):
        return f'{self.forum_name} ({self.id})'


class Email(Base):
    """ Model para armazenar emails para envio de alertas. """

    email = models.EmailField(unique=True)

    class Meta:
        """ Meta informações para a classe Email. """

        db_table            = f'{SCHEMA_NAME}email'
        verbose_name        = 'Email'
        verbose_name_plural = 'Emails'

    def __str__(self):
        return f'{self.email} ({self.id})'


class Alert(Base):
    """ Model para armazenar parâmetros de perfis de alertas criados. """

    name            = models.CharField(max_length=255)
    forums          = models.ManyToManyField(Forum)
    emails          = models.ManyToManyField(Email)
    keywords        = models.ManyToManyField(Keyword)
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

        db_table            = f'{SCHEMA_NAME}alert'
        verbose_name        = 'Alert'
        verbose_name_plural = 'Alerts'

    def __str__(self):
        return f'{self.name} ({self.id})'


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

        db_table            = f'{SCHEMA_NAME}post_alerted'
        verbose_name        = 'Post Alerted'
        verbose_name_plural = 'Posts Alerted'

    def __str__(self):
        return f'{self.title} ({self.id})'
