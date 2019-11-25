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
from app.models import Lab


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
		if not Role.objects.get(uid_id=userID, lid_id=labCode.lid_id):  #If the user doesn't already have a role for this lab
			obj = Role(lid_id=labCode.lid_id, uid_id=userID, role=labCode.role) #Add the role
			obj.save()
		else:
			raise forms.ValidationError(_('You are already a member of this lab'), code='invalid')

class CreateLabForm(forms.Form):
	labName = forms.CharField(required=True, max_length=75,
								widget=forms.TextInput({
									'class':'form-control',
									'placeholder':'Lab Name'}))
	labDescription = forms.CharField(required=True, max_length=150,
								widget=forms.TextInput({
									'class':'form-control',
									'placeholder':'Lab Description'}))

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(CreateLabForm, self).__init__(*args, **kwargs)

	def save(self):
		userID = self.user.id
		newLab = Lab(name=self.cleaned_data['labName'], description=self.cleaned_data['labDescription'])
		newLab.save()
		creatorRole = Role(lid_id=newLab.lid, uid_id=userID, role='p') #Add the professor role for the current user
		creatorRole.save()

class ManageLabForm(forms.Form):
	def __init__(self, *args, **kwargs):
		self.lid = kwargs.pop('lid', None)
		super(ManageLabForm, self).__init__(*args, **kwargs)

	labName = forms.CharField(required=False, max_length=75,
								widget=forms.TextInput({
									'class':'form-control'}))
	labDescription = forms.CharField(required=False, max_length=150,
								widget=forms.TextInput({
									'class':'form-control'}))

	def save(self):
		currentLab = Lab.objects.get(lid = self.lid)
		if (self.cleaned_data['labName'] != ""):  #If name updated
			Lab.objects.filter(lid=currentLab.lid).update(name=self.cleaned_data['labName'])

		if (self.cleaned_data['labDescription'] != ""):  #If description updated
			Lab.objects.filter(lid=currentLab.lid).update(description=self.cleaned_data['labDescription'])


