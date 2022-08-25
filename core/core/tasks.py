from todo.models import Task
from celery import Celery
from celery.schedules import crontab
app = Celery('core')





@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=10.0),
        delete_complete_tasks.s(),

    )


def delete_complete_tasks():
    instance = Task.objects.get(complete=True,)
    print(instance)
    instance.delete()
    return("task deleted")



