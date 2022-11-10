from task_manager import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        to=Position, on_delete=models.CASCADE, related_name="workers"
    )

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Task(models.Model):
    CHOICES = (
        ("Urgent", "Urgent"),
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
        ("Lowest", "Lowest"),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=15, choices=CHOICES, default="Lowest"
    )
    task_type = models.ForeignKey(
        to=TaskType, on_delete=models.CASCADE
    )
    assignees = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL, related_name="tasks"
    )

    def __str__(self) -> str:
        return (
            f"{self.name} {self.description} {self.priority} {self.task_type}"
        )
