"""
Classe para garantir permissões de modelo para ViewSets (para ser incluído juntamento com a autenticação JWT).

:created by:    Mateus Herrera
:created at:    2024-11-27

:updated by:    Mateus Herrera
:updated at:    2024-11-27
"""

from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets


class PermissionsMixins(viewsets.ModelViewSet):
    """ Mixin para verificar permissões de modelo para ViewSets. """

    def verificar_permissao(self, request, perm):
        """ Verifica se o usuário possui a permissão especificada. """

        if not request.user.has_perm(perm):
            raise PermissionDenied("Você não tem permissão para acessar este recurso.")

    def list(self, request, *args, **kwargs):
        """ Verifica permissão para listar objetos. """

        app = self.queryset.model._meta.app_label
        model = self.queryset.model._meta.model_name

        self.verificar_permissao(request, f'{app}.view_{model}')
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """ Verifica permissão para recuperar um objeto. """

        app = self.queryset.model._meta.app_label
        model = self.queryset.model._meta.model_name

        self.verificar_permissao(request, f'{app}.view_{model}')
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """ Verifica permissão para criar um objeto. """

        app = self.queryset.model._meta.app_label
        model = self.queryset.model._meta.model_name

        self.verificar_permissao(request, f'{app}.add_{model}')
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """ Verifica permissão para atualizar um objeto. """

        app = self.queryset.model._meta.app_label
        model = self.queryset.model._meta.model_name

        self.verificar_permissao(request, f'{app}.change_{model}')
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """ Verifica permissão para atualizar parcialmente um objeto. """

        app = self.queryset.model._meta.app_label
        model = self.queryset.model._meta.model_name

        self.verificar_permissao(request, f'{app}.change_{model}')
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """ Verifica permissão para deletar um objeto. """

        app = self.queryset.model._meta.app_label
        model = self.queryset.model._meta.model_name

        self.verificar_permissao(request, f'{app}.delete_{model}')
        return super().destroy(request, *args, **kwargs)

    pass