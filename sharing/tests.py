from django.test import TestCase
from sharing.models import User, Group, Resource, ResourceUserShare, ResourceGroupShare
from sharing.services import ResourceService


class ResourceServiceTest(TestCase):

    def setUp(self):
        # Users
        self.alice = User.objects.create(username="alice")
        self.bob = User.objects.create(username="bob")
        self.carol = User.objects.create(username="carol")

        # Groups
        self.group1 = Group.objects.create(name="group1")
        self.group2 = Group.objects.create(name="group2")

        # Add users to groups
        self.group1.members.add(self.alice, self.bob)
        self.group2.members.add(self.carol)

        # Resources
        self.resource1 = Resource.objects.create(name="Resource 1")
        self.resource2 = Resource.objects.create(name="Resource 2", shared_with_everyone=True)
        self.resource3 = Resource.objects.create(name="Resource 3")

        # Shares
        # Resource 1 shared directly with Alice and with group1 (which includes Alice and Bob)
        ResourceUserShare.objects.create(resource=self.resource1, user=self.alice)
        ResourceGroupShare.objects.create(resource=self.resource1, group=self.group1)

        # Resource 2 shared globally (everyone)
        # Resource 3 shared directly with Carol only
        ResourceUserShare.objects.create(resource=self.resource3, user=self.carol)

        self.service = ResourceService()

    def test_get_users_with_access_to_resource(self):
        # Resource 1 should have alice (direct) + alice,bob (group) = alice, bob distinct
        users_r1 = self.service.get_users_with_access_to_resource(self.resource1)
        usernames_r1 = set(u.username for u in users_r1)
        self.assertEqual(usernames_r1, {"alice", "bob"})

        # Resource 2 shared with everyone, so all users
        users_r2 = self.service.get_users_with_access_to_resource(self.resource2)
        usernames_r2 = set(u.username for u in users_r2)
        self.assertEqual(usernames_r2, {"alice", "bob", "carol"})

        # Resource 3 shared directly with Carol only
        users_r3 = self.service.get_users_with_access_to_resource(self.resource3)
        usernames_r3 = set(u.username for u in users_r3)
        self.assertEqual(usernames_r3, {"carol"})

    def test_get_resources_accessible_by_user(self):
        # Alice has resource1 (direct + group) and resource2 (global)
        resources_alice = self.service.get_resources_accessible_by_user(self.alice)
        resource_names_alice = set(r.name for r in resources_alice)
        self.assertEqual(resource_names_alice, {"Resource 1", "Resource 2"})

        # Bob has resource1 (group) and resource2 (global)
        resources_bob = self.service.get_resources_accessible_by_user(self.bob)
        resource_names_bob = set(r.name for r in resources_bob)
        self.assertEqual(resource_names_bob, {"Resource 1", "Resource 2"})

        # Carol has resource2 (global) and resource3 (direct)
        resources_carol = self.service.get_resources_accessible_by_user(self.carol)
        resource_names_carol = set(r.name for r in resources_carol)
        self.assertEqual(resource_names_carol, {"Resource 2", "Resource 3"})

    def test_get_resource_user_counts(self):
        results = self.service.get_resource_user_counts()
        counts = {item['resource'].name: item['user_count'] for item in results}

        # Resource 1: alice + bob (via group) = 2
        self.assertEqual(counts.get("Resource 1"), 2)

        # Resource 2: shared with everyone, so 3 users
        self.assertEqual(counts.get("Resource 2"), 3)

        # Resource 3: shared only with carol
        self.assertEqual(counts.get("Resource 3"), 1)

    def test_get_user_resource_counts(self):
        results = self.service.get_user_resource_counts()
        counts = {item['user'].username: item['resource_count'] for item in results}

        # Alice: resource1 (direct+group) + resource2(global) = 2
        self.assertEqual(counts.get("alice"), 2)

        # Bob: resource1 (group) + resource2(global) = 2
        self.assertEqual(counts.get("bob"), 2)

        # Carol: resource2(global) + resource3(direct) = 2
        self.assertEqual(counts.get("carol"), 2)
