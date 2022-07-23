from django.urls import path
from .views import (TaskList,
                    CreateTask, TaskEdit, TaskComplete, DeleteTask)
app_name = 'todo'
urlpatterns = [
    path('', TaskList.as_view(), name="list_task"),
    path('create', CreateTask.as_view(), name='create_task'),
    path('complete/<int:pk>', TaskComplete.as_view(), name='complete_task'),
    path('edit/<int:pk>', TaskEdit.as_view(), name='edit_task'),
    path('delete/<int:pk>', DeleteTask.as_view(), name='delete_task'),


]
