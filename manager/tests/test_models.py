from django.contrib.auth import get_user_model
from django.test import TestCase

from manager.models import TaskType, Position, Task


class ModelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        position = Position.objects.create(
            name="test",
        )

        task_type = TaskType.objects.create(
            name="test",
        )

        get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="Test first",
            last_name="Test last",
            position=position,
        )

        Task.objects.create(
            name="test",
            description="test12345",
            deadline="2022-11-11",
            is_completed=False,
            priority="High",
            task_type=task_type,
        )

    def test_task_type_str(self):
        task_type = TaskType.objects.get(id=1)
        self.assertEqual(str(task_type), task_type.name)

    def test_position_str(self):
        position = Position.objects.get(id=1)
        self.assertEqual(str(position), position.name)

    def test_worker_str(self):
        worker = get_user_model().objects.get(id=1)

        self.assertEqual(
            str(worker),
            f"{worker.first_name} {worker.last_name}, {worker.position}",
        )

    def test_task_str(self):
        task = Task.objects.get(id=1)

        self.assertEqual(
            str(task), f"{task.name} {task.description} {task.priority}"
        )

    def test_worker_with_position(self):
        username = "test"
        password = "test12345"
        first_name = "Test first"
        last_name = "Test last"
        position = Position.objects.get(id=1)
        worker = get_user_model().objects.get(id=1)

        self.assertEqual(worker.username, username)
        self.assertEqual(worker.first_name, first_name)
        self.assertEqual(worker.last_name, last_name)
        self.assertEqual(worker.position, position)
        self.assertTrue(worker.check_password(password), password)
