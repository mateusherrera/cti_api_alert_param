"""
Serializers para a aplicação de permissões

:created by:    Mateus Herrera
:created at:    2024-11-27

:updated by:    Mateus Herrera
:updated at:    2024-11-27
"""

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.apps import apps

from rest_framework import serializers


class UserPermissionsSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    groups = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'permissions', 'groups']
        pass

    def get_permissions(self, obj):
        ls_all_permissions = list(obj.get_all_permissions())
        dict_permissions = dict()

        # Não incluir no retorno
        django_apps = ['admin', 'auth', 'contenttypes', 'sessions', 'messages', 'staticfiles']

        for raw_permission in ls_all_permissions:
            app_permission = raw_permission.split('.')[0]
            permission = raw_permission.split('.')[1]

            if app_permission not in django_apps:
                type_permission = permission.split('_')[0]
                resource_name = permission.replace(type_permission + '_', '')

                content_type = ContentType.objects.get(model=resource_name)

                verbose_name = content_type.model_class()._meta.verbose_name
                verbose_name_plural = content_type.model_class()._meta.verbose_name_plural

                app_config = apps.get_app_config(app_permission)
                app_verbose_name = app_config.verbose_name

                if app_permission not in dict_permissions:
                    dict_permissions[app_permission] = dict()
                    dict_permissions[app_permission]['verbose_name'] = app_verbose_name

                if resource_name not in dict_permissions[app_permission]:
                    dict_permissions[app_permission][resource_name] = {
                        'verbose_name': verbose_name,
                        'vernose_name_plural': verbose_name_plural,
                        'permissions': {
                            'add': False,
                            'change': False,
                            'delete': False,
                            'view': False,
                        },
                    }
                    dict_permissions[app_permission] = dict(sorted(dict_permissions[app_permission].items()))
                dict_permissions[app_permission][resource_name]['permissions'][type_permission] = True


        return dict(sorted(dict_permissions.items()))

    pass
