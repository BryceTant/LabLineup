"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from app.models import Role
from app.models import LabCode

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Username'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class BootstrapRegisterForm(UserCreationForm):
	"""User registration form that uses Bootstrap CSS"""
	firstname = forms.CharField(required=True, max_length=254,
								widget=forms.TextInput({
									'class':'form-control',
									'placeholder':'First Name'}))
	lastname = forms.CharField(required=True, max_length=254,
								widget=forms.TextInput({
									'class':'form-control',
									'placeholder':'Last Name'}))
	username = forms.CharField(required=True, max_length=254,
								widget=forms.TextInput({
									'class':'form-control',
									'placeholder':'Username'}))
	password1 = forms.CharField(required=True,label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
	password2 = forms.CharField(required=True,label=_("Password Confirmation"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
	email = forms.EmailField(required=True,
								widget=forms.TextInput({
									'class':'form-control',
									'placeholder':'Email'}))

	class Meta:
		model = User
		fields = ("firstname", "lastname", "username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(BootstrapRegisterForm, self).save(commit=False)
		user.email = self.cleaned_data["email"]
		user.first_name = self.cleaned_data["firstname"]
		user.last_name = self.cleaned_data["lastname"]
		if commit:
			user.save()
		return user

class AddLabForm(forms.Form):
	labcode = forms.CharField(required=True, max_length=20,
								widget=forms.TextInput({
									'class':'form-control',
									'placeholder':'Lab Code'}))

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(AddLabForm, self).__init__(*args, **kwargs)

	def save(self):
		userID = self.user.id
		labCode = LabCode.objects.get(code=self.cleaned_data['labcode'])
		obj = Role(lid_id=labCode.lid_id, uid_id=userID, role=labCode.role) #Add the role
		obj.save()

class CreateLabForm(forms.Form):
    pass # TODO: implement        
