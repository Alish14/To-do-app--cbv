from todo.models import Task
from core.celery import app
from accounts.models import User


@app.task
def delete_complete_tasks():
        instance=Task.objects.filter(complete=True,)
        instance.delete()
        return("task deleted")

