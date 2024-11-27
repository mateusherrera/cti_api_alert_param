"""
Views para a aplicação de permissões.

:created by:    Mateus Herrera
:created at:    2024-11-27

:updated by:    Mateus Herrera
:updated at:    2024-11-27
"""

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status

from .serializers import UserPermissionsSerializer


class UserPermissionsView(generics.RetrieveAPIView):
    serializer_class = UserPermissionsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    pass
 

class ResourcePermissionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, resource_name):
        try:
            content_type = ContentType.objects.get(model=resource_name)
            permissions = Permission.objects.filter(content_type=content_type)

            verbose_name = content_type.model_class()._meta.verbose_name
            verbose_name_plural = content_type.model_class()._meta.verbose_name_plural

            permissions_response = {
                'verbose_name': verbose_name,
                'verbose_name_plural': verbose_name_plural,

                'permissions': {
                    'add': request.user.has_perm(f'{content_type.app_label}.add_{resource_name}'),
                    'change': request.user.has_perm(f'{content_type.app_label}.change_{resource_name}'),
                    'delete': request.user.has_perm(f'{content_type.app_label}.delete_{resource_name}'),
                    'view': request.user.has_perm(f'{content_type.app_label}.view_{resource_name}'),
                }
            }

            return Response(permissions_response, status=status.HTTP_200_OK)
        
        except ContentType.DoesNotExist:
            return Response({'detail': 'Recurso não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
    pass