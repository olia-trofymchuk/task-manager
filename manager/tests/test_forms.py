from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from manager.forms import WorkerCreationForm
from manager.models import Position, TaskType, Task


class WorkerFormsTest(TestCase):
    def setUp(self) -> None:
        position = Position.objects.create(
            name="test"
        )

        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="user12345test",
            first_name="Test first",
            last_name="Test last",
            position=position,
        )

        self.client.force_login(self.user)

    def test_worker_creation_form(self):
        form_data = {
            "username": "test",
            "password1": "user12345test",
            "password2": "user12345test",
            "first_name": "Test first",
            "last_name": "Test last",
            "position": Position.objects.get(id=1),
        }
        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_delete_worker(self):
        response = self.client.post(
            reverse("manager:worker-delete", kwargs={"pk": self.user.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(get_user_model().objects.filter(id=self.user.id).exists())

    def test_search_worker(self):
        response = self.client.get(reverse("manager:worker-list") + "?username=e")
        workers = get_user_model().objects.filter(username__icontains="e")

        self.assertEqual(list(response.context["worker_list"]), list(workers))
        self.assertEqual(len(workers), 1)


class PositionFormsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="user12345test",
        )

        self.client.force_login(self.user)

    def test_position_create(self):
        form_data = {
            "name": "test"
        }
        response = self.client.post(
            reverse("manager:position-create"), data=form_data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Position.objects.get(id=1).name, form_data["name"])

    def test_delete_position(self):
        position = Position.objects.create(
            name="QA"
        )
        response = self.client.post(
            reverse("manager:position-delete", kwargs={"pk": position.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Position.objects.filter(id=position.id).exists())

    def test_search_position(self):
        Position.objects.create(
            name="test"
        )

        response = self.client.get(reverse("manager:position-list") + "?name=e")
        positions = Position.objects.filter(name__icontains="e")

        self.assertEqual(list(response.context["position_list"]), list(positions))
        self.assertEqual(len(positions), 1)


class TaskTypeFormsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="user12345test",
        )

        self.client.force_login(self.user)

    def test_task_type_create(self):
        form_data = {
            "name": "test"
        }
        response = self.client.post(
            reverse("manager:task-type-create"), data=form_data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TaskType.objects.get(id=1).name, form_data["name"])

    def test_delete_task_type(self):
        task_type = TaskType.objects.create(
            name="Bug"
        )
        response = self.client.post(
            reverse("manager:task-type-delete", kwargs={"pk": task_type.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(TaskType.objects.filter(id=task_type.id).exists())

    def test_search_task_type(self):
        TaskType.objects.create(
            name="test"
        )

        response = self.client.get(reverse("manager:task-type-list") + "?name=e")
        task_types = TaskType.objects.filter(name__icontains="e")

        self.assertEqual(list(response.context["tasktype_list"]), list(task_types))
        self.assertEqual(len(task_types), 1)


class TaskFormsTest(TestCase):
    def setUp(self) -> None:
        TaskType.objects.create(
            name="Bug",
        )

        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="user12345test",
        )

        self.client.force_login(self.user)

    def test_search_task_type(self):
        TaskType.objects.create(
            name="test",
        )

        Task.objects.create(
            name="test1",
            description="description test",
            deadline="2023-01-01",
            is_completed=False,
            priority="Low",
            task_type=TaskType.objects.get(id=1),
        )

        response = self.client.get(reverse("manager:task-list") + "?name=e")
        tasks = Task.objects.filter(name__icontains="e")

        self.assertEqual(list(response.context["task_list"]), list(tasks))
        self.assertEqual(len(tasks), 1)
