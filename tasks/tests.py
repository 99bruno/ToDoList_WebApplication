from django.test import TestCase
from .models import Task


class TaskModelTest(TestCase):
    def setUp(self):
        Task.objects.create(title="Test Task", description="Just a test task")

    def test_task_creation(self):
        task = Task.objects.get(title="Test Task")
        self.assertEqual(task.description, "Just a test task")
