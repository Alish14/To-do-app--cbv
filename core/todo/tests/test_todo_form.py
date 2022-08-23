from django.test import SimpleTestCase
from todo.forms import TaskUpdate


class TestTaskForm(SimpleTestCase):
    def test_task_update_form_with_data(self):
        form = TaskUpdate(data={"title": "test"})
        self.assertTrue(form.is_valid())

    def test_task_update_form_with_no_data(self):
        form = TaskUpdate(data={})
        self.assertFalse(form.is_valid())
