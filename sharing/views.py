from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Resource, User
from .serializers import UserSerializer, ResourceSerializer
from .services import ResourceService


class BaseView(APIView):
    RESOURCE_VIEW = ResourceService()

    def handle_exception(self, exc):
        if isinstance(exc, Resource.DoesNotExist):
            return Response({'detail': 'Resource not found'}, status=status.HTTP_404_NOT_FOUND)
        elif isinstance(exc, User.DoesNotExist):
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)


class ResourceAccessListView(BaseView):

    @swagger_auto_schema(
        operation_summary="List users with access to a resource",
        responses={200: 'List of users'}
    )
    def get(self, request, resource_id):
        try:
            resource = Resource.objects.get(id=resource_id)
        except Resource.DoesNotExist:
            return Response({'detail': 'Resource not found'}, status=status.HTTP_404_NOT_FOUND)

        users = self.RESOURCE_VIEW.get_users_with_access_to_resource(resource)
        serializer = UserSerializer(users, many=True)

        return Response({'users': serializer.data})


class UserResourceListView(BaseView):

    @swagger_auto_schema(
        operation_summary="List resources accessible to a user",
        responses={200: 'List of resources'}
    )
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        resources = self.RESOURCE_VIEW.get_resources_accessible_by_user(user)
        serializer = ResourceSerializer(resources, many=True)
        return Response({'resources': serializer.data})


class ResourceUserCountView(BaseView):

    @swagger_auto_schema(
        operation_summary="Count of users with access to each resource",
        responses={200: 'List of resources with user counts'}
    )
    def get(self, request):
        result = self.RESOURCE_VIEW.get_resource_user_counts()
        data = [{'resource': ResourceSerializer(entry['resource']).data, 'user_count': entry['user_count']}
                for entry in result]
        return Response({'resources': data})


class UserResourceCountView(BaseView):

    @swagger_auto_schema(
        operation_summary="Count of resources accessible to each user",
        responses={200: 'List of users with resource counts'}
    )
    def get(self, request):
        result = self.RESOURCE_VIEW.get_user_resource_counts()
        data = [{'user': UserSerializer(entry['user']).data, 'resource_count': entry['resource_count']}
                for entry in result]
        return Response({'users': data})
