from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    members = models.ManyToManyField(User, related_name='members_group')


class Resource(models.Model):
    name = models.CharField(max_length=255)
    shared_with_everyone = models.BooleanField(default=False)


class ResourceUserShare(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name="user_shares")
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ResourceGroupShare(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name="group_shares")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
