from django.forms import ModelForm
from .models import Task
from django import forms


class TaskUpdate(ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control rounded-4",
                "name": "title",
                "placeholder": "enter the title",
            }
        ),
        label="What do you need to do today?",
    )

    class Meta:
        model = Task
        fields = ("title",)
