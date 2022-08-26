from todo.models import Task
from celery import Celery
from celery.schedules import crontab
app = Celery('core')


@app.task(bind=True)
def delete_complete_tasks():
    instance = Task.objects.get(complete=True,)
    print(instance)
    instance.delete()
    return("task deleted")



