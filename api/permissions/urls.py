"""
URLs para permissões de usuários.

:created by:    Mateus Herrera
:created at:    2024-11-27

:updated by:    Mateus Herrera
:updated at:    2024-11-27
"""

from django.urls import path

from .views import (
    UserPermissionsView,
    ResourcePermissionsView
)


urlpatterns = [
    path('permissions/', UserPermissionsView.as_view()),
    path('permissions/<str:resource_name>/', ResourcePermissionsView.as_view()),
]
