from todo.models import Task
from celery import Celery
from celery import shared_task

app = Celery('core')

@shared_task
def delete_complete_tasks():
    instance = Task.objects.get(complete=True,)
    print(instance)
    instance.delete()
    return("task deleted")



