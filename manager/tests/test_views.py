from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from manager.models import TaskType, Position, Task

TASK_TYPE_LIST_URL = reverse("manager:task-type-list")
TASK_TYPE_CREATE_URL = reverse("manager:task-type-create")
WORKER_URL = reverse("manager:worker-create")
WORKER_LIST_URL = reverse("manager:worker-list")
TASK_LIST_URL = reverse("manager:task-list")
TASK_URL = reverse("manager:task-create")
POSITION_LIST_URL = reverse("manager:position-list")
POSITION_CREATE_URL = reverse("manager:position-create")


class PublicTests(TestCase):
    def test_login_required(self):
        response_task_type = self.client.get(TASK_TYPE_LIST_URL)
        response_worker = self.client.get(WORKER_LIST_URL)
        response_task = self.client.get(TASK_LIST_URL)
        response_position = self.client.get(POSITION_LIST_URL)

        self.assertNotEqual(response_task_type.status_code, 200)
        self.assertNotEqual(response_worker.status_code, 200)
        self.assertNotEqual(response_task.status_code, 200)
        self.assertNotEqual(response_position.status_code, 200)


class PrivateTaskTypeTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test", "password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_task_types(self):
        TaskType.objects.create(name="Bug")
        TaskType.objects.create(name="QA")

        response = self.client.get(TASK_TYPE_LIST_URL)

        task_types = TaskType.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["tasktype_list"]), list(task_types)
        )
        self.assertTemplateUsed(response, "manager/tasktype_list.html")

    def test_create_task_type(self):
        name = "Bug"

        form_data = {"name": name}

        self.client.post(TASK_TYPE_CREATE_URL, data=form_data)
        task_type = TaskType.objects.get(name=name)

        self.assertEqual(task_type.name, name)


class PrivateWorkerTest(TestCase):
    def setUp(self):
        position = Position.objects.create(
            name="DevOps",
        )

        self.user = get_user_model().objects.create_user(
            "test", "password123", position=position,
        )
        self.client.force_login(self.user)

    def test_create_worker(self):
        position = Position.objects.get(id=1)

        form_data = {
            "username": "test",
            "password1": "password123",
            "password2": "password123",
            "position": position,
        }

        self.client.post(WORKER_URL, data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.username, form_data["username"])
        self.assertEqual(new_user.position, form_data["position"])

    def test_retrieve_workers(self):
        position = Position.objects.create(
            name="Developer"
        )
        get_user_model().objects.create_user(
            username="test1", password="test12345", position=position,
        )
        get_user_model().objects.create_user(
            username="test2", password="test12345", position=position,
        )

        response = self.client.get(WORKER_LIST_URL)

        workers = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["worker_list"]), list(workers))

        self.assertTemplateUsed(response, "manager/worker_list.html")


class PrivatePositionTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test", "password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_position(self):
        Position.objects.create(name="DevOps")
        Position.objects.create(name="Developer")

        response = self.client.get(POSITION_LIST_URL)

        positions = Position.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["position_list"]), list(positions)
        )
        self.assertTemplateUsed(response, "manager/position_list.html")

    def test_create_position(self):
        name = "Designer"

        form_data = {"name": name}

        self.client.post(POSITION_CREATE_URL, data=form_data)
        position = Position.objects.get(name=name)

        self.assertEqual(position.name, name)


class PrivateTaskTest(TestCase):
    def setUp(self):
        TaskType.objects.create(
            name="test",
        )

        Task.objects.create(
            name="test2",
            description="description test",
            deadline="2024-01-01",
            is_completed=True,
            priority="High",
            task_type=TaskType.objects.get(id=1),
        )

        self.user = get_user_model().objects.create_user(
            "test", "password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_task(self):
        Task.objects.create(
            name="test1",
            description="description test",
            deadline="2023-01-01",
            is_completed=False,
            priority="Low",
            task_type=TaskType.objects.get(id=1),
        )

        response = self.client.get(TASK_LIST_URL)

        tasks = Task.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["task_list"]), list(tasks))

        self.assertTemplateUsed(response, "manager/task_list.html")

    def test_create_task(self):
        form_data = {
            "name": "test2",
            "description": "description test",
            "deadline": "2024-01-01",
            "is_completed": False,
            "priority": "High",
            "task_type": TaskType.objects.get(id=1),
        }

        self.client.post(TASK_URL, data=form_data)
        new_task = Task.objects.get(name=form_data["name"])

        self.assertEqual(new_task.name, form_data["name"])
        self.assertEqual(new_task.priority, form_data["priority"])
