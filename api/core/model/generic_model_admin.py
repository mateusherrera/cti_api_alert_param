"""
Base para o ModelAdmin genérico.

:created by:    Mateus Herrera
:created at:    2025-07-18
"""

from django.contrib import admin
from django.db      import models


class GenericModelAdmin(admin.ModelAdmin):
    """ Classe base para ModelAdmin genérico, configurando exibição de campos """

    filterable_field_types = (
        models.BooleanField,
        models.NullBooleanField,
        models.DateField,
        models.DateTimeField,
        models.ForeignKey,
        models.ManyToManyField,
        models.DecimalField,
        models.IntegerField,
    )
    searchable_field_types = (
        models.CharField,
        models.TextField,
    )

    def __init__(self, model, admin_site):
        """ Inicializa o ModelAdmin genérico, configurando exibição de campos. """

        # gera lista de todos os campos, menos os excluídos
        fields = [
            f for f in model._meta.fields
            if f.name not in self.exclude_fields
        ]

        # list_display: todo mundo
        self.list_display = [f.name for f in fields]

        # list_filter: só os tipos definidos em filterable_field_types
        self.list_filter = [
            f.name for f in fields
            if isinstance(f, self.filterable_field_types)
        ]

        # search_fields: só texto
        self.search_fields = [
            f.name for f in fields
            if isinstance(f, self.searchable_field_types)
        ]

        super().__init__(model, admin_site)
