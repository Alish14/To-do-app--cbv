from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from todo.views import TaskComplete, TaskEdit, DeleteTask, CreateTask


class TestUrl(SimpleTestCase):
    def test_todo_Task_complete_url(self):
        url = reverse("todo:complete_task", kwargs={"pk": 2})
        self.assertEqual(resolve(url).func.view_class, TaskComplete)

    def test_todo_Task_edit_url(self):
        url = reverse("todo:edit_task", kwargs={"pk": 2})
        self.assertEqual(resolve(url).func.view_class, TaskEdit)

    def test_todo_Task_delete_url(self):
        url = reverse("todo:delete_task", kwargs={"pk": 2})
        self.assertEqual(resolve(url).func.view_class, DeleteTask)

    def test_todo_Task_Create_url(self):
        url = reverse("todo:create_task")
        self.assertEqual(resolve(url).func.view_class, CreateTask)
