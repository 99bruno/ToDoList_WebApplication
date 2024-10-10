# tasks/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Task(models.Model):
    """
    Represents a task in the task management system.

    Attributes:
        id (int): The primary key for the task.
        user (User): The user to whom the task is assigned.
        title (str): The title of the task.
        description (str): A detailed description of the task.
        tag (TagTask): The tag associated with the task.
        date (datetime): The date and time when the task was created.
        completed (bool): Indicates whether the task is completed.
    """

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    tag = models.ForeignKey('TagTask', on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class TagTask(models.Model):
    """
    Represents a tag associated with tasks in the task management system.

    Attributes:
        id (int): The primary key for the tag.
        user_id (User): The user to whom the tag is assigned.
        tag_name (str): The name of the tag.
    """

    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)
    tag_name = models.CharField(max_length=200)

    def __str__(self):
        return self.tag_name
