from django.shortcuts import redirect
from .models import Task
from .forms import TaskUpdate
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


"""
TaskList View for show user Task and user Task model 
"""


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    ordering = "create_date"
    template_name = "todo/list_task.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user=self.request.user)
        context["count"] = context["tasks"].filter(complete=False).count()
        search_input = self.request.GET.get("search-area") or ""
        if search_input:
            context["tasks"] = context["tasks"].filter(title__contains=search_input)

        context["search_input"] = search_input

        return context


"""    
CreateTask  : User model task for Create user task by form

"""


class CreateTask(LoginRequiredMixin, CreateView):
    model = Task
    fields = ("title",)
    success_url = reverse_lazy("todo:list_task")
    template_name = "todo/list_task.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTask, self).form_valid(form)


"""
 TaskEdit: Edit User Task 
 
"""


class TaskEdit(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskUpdate
    success_url = reverse_lazy("todo:list_task")
    template_name = "todo/update_task.html"


"""

TaskComplete:Task Create User Task
"""


class TaskComplete(LoginRequiredMixin, View):
    model = Task
    success_url = reverse_lazy("todo:list_task")

    def get(self, request, *args, **kwargs):
        object = Task.objects.get(id=kwargs.get("pk"))
        object.complete = True
        object.save()
        return redirect(self.success_url)


"""
DeleteTask: Delete User Task
"""


class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("todo:list_task")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
