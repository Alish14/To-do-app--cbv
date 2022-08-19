from django import forms
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()


class RegistrationForm(UserCreationForm):
	email = forms.EmailField(
		max_length=254, help_text='Required. Add a valid email address.')

	class Meta:
		model = User
		fields = ('email', 'nickname', 'password1', 'password2', )

	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			account = User.objects.exclude(pk=self.instance.pk).get(email=email)
		except User.DoesNotExist:
			return email
		raise forms.ValidationError('Email "%s" is already in use.' % account)

	def clean_username(self):
		nickname = self.cleaned_data['nickname']
		try:
			user = User.objects.exclude(
				pk=self.instance.pk).get(nickname=nickname)
		except User.DoesNotExist:
			return nickname
		raise forms.ValidationError('nickname "%s" is already in use.' % nickname)


