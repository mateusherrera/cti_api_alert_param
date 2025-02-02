"""
Cofigurações de administração do Django para o aplicativo alert_param.

:created by:    Mateus Herrera
:created at:    2024-10-25
"""

from django.contrib import admin

from alert_param.models import (
    Alert,
    Forum,
    Email,
    Keyword,
)


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    """ Configurações de administração para o modelo Forum. """

    list_display = (
        'id',
        'forum_name'
    )

    pass


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    """ Configurações de administração para o modelo Email. """

    list_display = (
        'id',
        'email'
    )

    pass


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    """ Configurações de administração para o modelo Alert. """

    list_display = (
        'id',
        'is_active',
        'id_user',
        'start_date',
        'final_date',
        'qte_frequency',
        'type_frequency',
        'is_relevant',
        'last_run',
        'run'
    )

    pass


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    """ Configurações de administração para o modelo Keyword. """

    list_display = (
        'id',
        'word'
    )

    pass
