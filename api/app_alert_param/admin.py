"""
Cofigurações de administração do Django para o aplicativo app_alert_param.

:created by:    Mateus Herrera
:created at:    2024-10-25
"""

from django.apps    import apps
from django.contrib import admin

from core.model.generic_model_admin import GenericModelAdmin


app_label = 'app_alert_param'

for model in apps.get_app_config(app_label).get_models():
    exclude = ()

    # Cria uma classe ModelAdmin dinâmica
    admin_class = type(
        f'{model.__name__}Admin',
        (GenericModelAdmin,),
        {'exclude_fields': exclude}
    )

    # Registra no admin
    admin.site.register(model, admin_class)
