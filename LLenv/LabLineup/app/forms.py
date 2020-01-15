"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from app.models import Role
from app.models import LabCode
from app.models import Lab
from app.models import Request
from app.models import Notify
import datetime


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

class ChangePasswordForm(PasswordChangeForm):
    """Form to change user password"""
    old_password = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput({
                                    'class':'form-control',
                                    'placeholder':'Old Password'}))
    new_password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput({
                                    'class':'form-control',
                                    'placeholder':'New Password'}))
    new_password2 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput({
                                    'class':'form-control',
                                    'placeholder':'New Password'}))


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

    def is_valid(self):
        baseValid = super().is_valid()
        queryEmail = None
        try:
            queryEmail = User.objects.get(email=self.cleaned_data["email"])
        except:
            pass
        if (queryEmail == None):
            pass
        else:
            baseValid = False
            self.add_error(field="email",error="Email has already been used")
        queryUsername = None
        try:
            queryUsername = User.objects.get(username=self.cleaned_data["username"])
        except:
            pass
        if (queryEmail == None):
            pass
        else:
            baseValid = False
            self.add_error(field="username", error="The username has already been taken")
        return baseValid

    def save(self, commit=True):
        user = super(BootstrapRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["firstname"]
        user.last_name = self.cleaned_data["lastname"]
        user.is_active = False  # Account won't be active until email is confirmed
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
        noRole = True
        try:
            Role.objects.get(uid_id=userID, lid_id=labCode.lid_id)
            noRole = False
        except:
            pass  #Error handled in form Validation
        if noRole:  #If the user doesn't already have a role for this lab
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
        return newLab.lid

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

class SubmitRequestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.lid = kwargs.pop('lid', None)
        super(SubmitRequestForm, self).__init__(*args, **kwargs)

    station = forms.CharField(required=True, max_length=10,
                                widget=forms.TextInput({
                                    'class':'form-control',
                                    'placeholder':'Station'}))
    description = forms.CharField(required=True, max_length=250,
                                widget=forms.Textarea({
                                    'class':'form-control',
                                    'rows' : 6,
                                    'placeholder':'Problem Description'}))

    def save(self):
        userID = self.user.id
        labID = self.lid
        newStation = self.cleaned_data['station']
        newDescription = self.cleaned_data['description']
        newRequest = Request(station=newStation, description=newDescription, timeSubmitted=datetime.datetime.now(),
                       timeCompleted=None, feedback=None, huid_id=None, lid_id=labID, suid_id=userID)
        newRequest.save()
        return newRequest.rid #Must return rid to be set to session variable

class EditAccountDetailsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(EditAccountDetailsForm, self).__init__(*args, **kwargs)

    firstname = forms.CharField(required=False, max_length=30,
                                widget=forms.TextInput({
                                    'class':'form-control'}))
    lastname = forms.CharField(required=False, max_length=150,
                                widget=forms.TextInput({
                                    'class':'form-control'}))
    email = forms.EmailField(required=False,
                                widget=forms.TextInput({
                                    'class':'form-control'}))

    def save(self):
        userID = self.user.id
        if self.cleaned_data['firstname'] != self.user.first_name: #If first name updated
            User.objects.filter(id=userID).update(first_name=self.cleaned_data['firstname'])
        if self.cleaned_data['lastname'] != self.user.last_name: #If last name updated
            User.objects.filter(id=userID).update(last_name=self.cleaned_data['lastname'])
        if self.cleaned_data['email'] != self.user.email: #If email updated
            User.objects.filter(id=userID).update(email=self.cleaned_data['email'])

class ResetPasswordForm(forms.Form):
    """Form to reset user password"""
    new_password1 = forms.CharField(label=_("New Password"),
                                    widget=forms.PasswordInput({
                                    'class':'form-control',
                                    'placeholder':'New Password'}))
    new_password2 = forms.CharField(label=_("New Password"),
                                    widget=forms.PasswordInput({
                                    'class':'form-control',
                                    'placeholder':'Repeat New Password'}))

    def save(self):
        if (self.cleaned_data["new_password1"] == self.cleaned_data["new_password2"]):
            return self.cleaned_data["new_password1"]
        else:
            return False

class ForgotPasswordForm(forms.Form):
    """Form to send password reset link to email"""
    email = forms.EmailField(label=_("Email"),
                                    widget=forms.TextInput({
                                    'class':'form-control',
                                    'placeholder':'Your Email'}))

    def save(self):
        return self.cleaned_data["email"]

class ManageLabNotificationsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.lid = kwargs.pop('lid', None)
        super(ManageLabNotificationsForm, self).__init__(*args, **kwargs)

    notifyNew = forms.BooleanField(required = False)

    notifyThreshold = forms.IntegerField(required = False)

    def save(self):
        currentLab = Lab.objects.get(lid = self.lid)
        Notify.objects.filter(lid_id=currentLab.lid, uid_id=self.user).update(notifyNew = self.cleaned_data["notifyNew"],
                                                                              notifyThreshold = self.cleaned_data["notifyThreshold"])

        query = Notify.objects.filter(lid_id=currentLab.lid, uid_id=self.user)
        print (query)
