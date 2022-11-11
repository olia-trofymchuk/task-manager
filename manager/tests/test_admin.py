from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from manager.models import Position


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="test_pass123"
        )
        self.client.force_login(self.admin_user)

        position = Position.objects.create(
            name="test",
        )

        self.worker = get_user_model().objects.create_user(
            username="test",
            password="test_pass123",
            first_name="test first",
            last_name="test last",
            position=position,
        )

    def test_worker_position_in_list(self):
        url = reverse("admin:manager_worker_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.worker.position)

    def test_worker_position_in_detailed_list(self):
        url = reverse("admin:manager_worker_change", args=[self.worker.id])
        response = self.client.get(url)

        self.assertContains(response, self.worker.position)
