from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

class AccountAuthenticationForm(ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']
