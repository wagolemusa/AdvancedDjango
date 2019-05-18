from django import forms

from django.contrib.auth import(
	authenticate,
	get_user_model,
	login,
	logout,
	)

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)


	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")

		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("This user does not exist")
			if not user.check_password(password):
				raise forms.ValidationError("Incorrent password")
			if not user.is_active:
				raise form.ValidationError("This user is longer active.")
		return super(UserLoginForm, self).clean(*args, **kwargs)