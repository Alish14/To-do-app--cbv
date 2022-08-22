from django.test import TestCase
from todo.models import Task


class Test_Todo_TaskModel(TestCase):
    def test_create_task_with_ValidData(self):
        task = Task.objects.create(title="test", complete=True)
        self.assertTrue(Task.objects.filter(pk=task.id).exists)
