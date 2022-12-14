from django.urls import reverse

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

    class Meta:
        ordering = ["name"]


class Worker(AbstractUser):
    position = models.ForeignKey(
        to=Position, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"
        ordering = ["first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.position}"

    def get_absolute_url(self):
        return reverse("manager:worker-detail", kwargs={"pk": self.pk})


class Task(models.Model):
    CHOICES = (
        ("1 - Urgent", "1 - Urgent"),
        ("2 - High", "2 - High"),
        ("3 - Medium", "3 - Medium"),
        ("4 - Low", "4 - Low"),
        ("5 - Lowest", "5 - Lowest"),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=15, choices=CHOICES, default="5 - Lowest"
    )
    task_type = models.ForeignKey(to=TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL, related_name="tasks"
    )

    class Meta:
        ordering = ["is_completed", "priority", "deadline"]

    def __str__(self) -> str:
        return f"{self.name} {self.description} {self.priority}"
