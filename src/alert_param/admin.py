"""
Cofigurações de administração do Django para o aplicativo alert_param.

:author: Mateus Herrera Gobetti Borges
:github: mateusherrera

:created at: 2024-09-25
:updated at: 2024-09-25
"""

from django.contrib import admin

from .models import (
    Alert,
    Keyword,
    Forum,
    Email,
)


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    """ Configurações de administração para o modelo Keyword. """

    list_display = (
        'id',
        'word'
    )

    pass


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
        'run'
    )

    pass
