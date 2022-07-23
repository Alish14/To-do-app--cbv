from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login,logout
from django.shortcuts import redirect
from django.views.generic import View


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    fields = "username","password"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("todo:list_task")


class RegisterPage(FormView):
    template_name = "accounts/register.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("todo:list_task")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("todo:list_task")
        return super(RegisterPage, self).get(*args, **kwargs)
class LogoutView(View):
    def get(self, request):
        logout(request)
        return  reverse_lazy("accounts:login")
