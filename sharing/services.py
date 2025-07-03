from sharing.models import Resource, Users


class ResourceService:

    def get_resource_user_counts(self):
        results = []
        for resource in Resource.objects.all():
            users = self.get_users_with_access_to_resource(resource)
            results.append({
                'resource': resource,
                'user_count': users.count()
            })

        return results

    def get_user_resource_counts(self):
        users = Users.objects.all()
        results = []

        for user in users:
            resources = self.get_resources_accessible_by_user(user)
            results.append({
                'user': user,
                'resource_count': resources.count()
            })

        return results

    def get_users_with_access_to_resource(self, resource):
        if resource.shared_with_everyone:
            return Users.objects.all()

        direct_user_ids = resource.user_shares.values_list('user_id', flat=True)

        group_ids = resource.group_shares.values_list('group_id', flat=True)
        group_user_ids = Users.objects.filter(members_group__id__in=group_ids).values_list('id', flat=True)
        all_user_ids = set(direct_user_ids) | set(group_user_ids)

        return Users.objects.filter(id__in=all_user_ids)

    def get_resources_accessible_by_user(self, user):
        if user.is_superuser:
            return Resource.objects.all()

        direct = Resource.objects.filter(user_shares__user=user)
        group = Resource.objects.filter(group_shares__group__members=user)
        global_shared = Resource.objects.filter(shared_with_everyone=True)

        return (direct | group | global_shared).distinct()
