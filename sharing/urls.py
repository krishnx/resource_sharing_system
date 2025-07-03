from django.urls import path
from .views import (
    ResourceAccessListView,
    UserResourceListView,
    ResourceUserCountView,
    UserResourceCountView,
)

urlpatterns = [
    path('resource/<int:resource_id>/access-list', ResourceAccessListView.as_view()),
    path('user/<int:user_id>/resources', UserResourceListView.as_view()),
    path('resources/with-user-count', ResourceUserCountView.as_view()),
    path('users/with-resource-count', UserResourceCountView.as_view()),
]
