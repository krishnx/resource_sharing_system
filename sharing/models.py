from django.db import models


class Users(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    members = models.ManyToManyField(Users, related_name='members_group')

    def __str__(self):
        return self.name


class Resource(models.Model):
    name = models.CharField(max_length=255)
    shared_with_everyone = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ResourceUserShare(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='user_shares')
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.name} shares {self.resource.name}'


class ResourceGroupShare(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='group_shares')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.group.name} shares {self.resource.name}' if self.group else f'Global share of {self.resource.name}'
