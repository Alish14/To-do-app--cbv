from django.shortcuts import render,redirect
from .models import Task
from .forms import TaskUpdate
from django.views.generic import (ListView,CreateView,UpdateView,DeleteView)
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class TaskList(LoginRequiredMixin,ListView):
    model=Task
    context_object_name="tasks"
    ordering="create_date"
    template_name="todo/list_task.html"
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

class CreateTask(LoginRequiredMixin,CreateView):
    model=Task
    fields = ("title",)
    success_url = reverse_lazy("todo:list_task")
    template_name="todo/list_task.html"
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(CreateTask, self).form_valid(form)
 
class TaskEdit(LoginRequiredMixin,UpdateView):
    model=Task
    form_class=TaskUpdate
    success_url = reverse_lazy("todo:list_task")
    template_name="todo/update_task.html"


class TaskComplete(LoginRequiredMixin,View):
    model = Task
    success_url = reverse_lazy("todo:list_task")
    
    def get(self, request, *args, **kwargs):
        object = Task.objects.get(id=kwargs.get("pk"))
        object.complete = True
        object.save()
        return redirect(self.success_url)


class DeleteTask(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("todo:list_task")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
