"""
Definition of forms.
"""

from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.password_validation import password_validators_help_text_html
from django.core.validators import EmailValidator
from app.models import Role
from app.models import LabCode
from app.models import Lab
from app.models import Request
from app.models import Notify
import datetime
from pytz import utc as utc


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

    class Meta:
        model = User
        fields = ("username", "password")

    def is_valid(self):
        baseValid = super().is_valid()
        queryUser = None
        try:
            queryUser = User.objects.get(username=self.cleaned_data["username"])
            if queryUser.is_active == False:
                baseValid = False
                self.add_error(field="username", error="You have not confirmed your email")
        except:
            pass
        return baseValid

class ChangePasswordForm(PasswordChangeForm):
    """Form to change user password"""
    old_password = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput({
                                    'class':'form-control',
                                    'placeholder':'Old Password'}))
    new_password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput({
                                    'class':'form-control',
                                    'placeholder':'New Password'}),
                                help_text=password_validators_help_text_html())
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

    def is_valid(self):
        baseValid = super().is_valid()
        #See if LabCode exists
        queryLabCode = None
        try:
            queryLabCode = LabCode.objects.get(code=self.cleaned_data['labcode'])
        except:
            self.add_error(field="labcode", error="The lab code you enter does not exist")
            baseValid = False
            return baseValid
        #See if the user already has a role in that lab
        queryRole = None
        try:
            Role.objects.get(uid_id=self.user.id, lid_id=queryLabCode.lid_id)
            self.add_error(field="labcode", error="You are already a member of this lab")
            baseValid = False
            return baseValid
        except:
            pass
        #See if the lab is marked as open or closed
        queryLab = None
        try:
            queryLab = Lab.objects.get(lid=queryLabCode.lid_id)
            if not queryLab.open:
                self.add_error(field="labcode", error="The professor has closed this lab")
                baseValid = False
        except:
            pass
        return baseValid


    def save(self):
        userID = self.user.id
        labCode = LabCode.objects.get(code=self.cleaned_data['labcode'])
        obj = Role(lid_id=labCode.lid_id, uid_id=userID, role=labCode.role) #Add the role
        obj.save()

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
        newLab = Lab(name=self.cleaned_data['labName'],
                    description=self.cleaned_data['labDescription'])
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
    taViewFeedback = forms.BooleanField(required = False)
    open = forms.BooleanField(required=False)

    def save(self):
        currentLab = Lab.objects.get(lid = self.lid)
        if (self.cleaned_data['labName'] != ""):  #If name updated
            Lab.objects.filter(lid=currentLab.lid).update(name=self.cleaned_data['labName'])

        if (self.cleaned_data['labDescription'] != ""):  #If description updated
            Lab.objects.filter(lid=currentLab.lid).update(description=self.cleaned_data['labDescription'])
        Lab.objects.filter(lid=currentLab.lid).update(taViewFeedback=self.cleaned_data['taViewFeedback'],
                                                      open=self.cleaned_data['open'])

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
        newRequest = Request(station=newStation, description=newDescription, timeSubmitted=datetime.datetime.now(utc),
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

    def is_valid(self):
        baseValid = super().is_valid()
        emailValid = True
        try:
            emailValidator = EmailValidator(message="The email you entered is not valid")
            emailValidator(self.cleaned_data["email"])
        except:
            emailValid = False
        if len(self.cleaned_data["email"]) == 0:
            emailValid = False
            self.add_error("email", "Your email cannot be blank")
        if (not emailValid):
            baseValid = False
        if len(self.cleaned_data["firstname"]) == 0:
            baseValid = False
            self.add_error("firstname", "Your first name cannot be blank")
        if len(self.cleaned_data["lastname"]) == 0:
            baseValid = False
            self.add_error("lastname", "Your last name cannot be blank")
        return baseValid

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
    def is_valid(self):
        baseValid = super().is_valid()
        invalidPass = False
        if self.cleaned_data["new_password1"] != self.cleaned_data["new_password2"]:
            baseValid = False
            self.add_error(field="new_password2", error="The passwords you entered don't match")
        try:
            invalidPass = validate_password(self.cleaned_data["new_password1"])
        except:
            pass
        if invalidPass != None:
            baseValid = False
            self.add_error(field="new_password1", error="The password you \
                entered doesn't meet the minimum requirements. Your password\
                must be at least 8 characters in length, cannot contain only \
                numbers, cannot be similiar to your username, name, or email, \
                and cannot be a common password.")
        return baseValid

    def save(self):
        return self.cleaned_data["new_password1"]

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

    def is_valid(self):
        baseValid = super().is_valid()
        if self.cleaned_data["notifyThreshold"] < 0:
            baseValid = False
            self.add_error(field="notifyThreshold", error="The threshold must be 0 or greater")
        return baseValid

    def save(self):
        currentLab = Lab.objects.get(lid = self.lid)
        Notify.objects.filter(lid_id=currentLab.lid, uid_id=self.user).update(notifyNew = self.cleaned_data["notifyNew"],
                                                                              notifyThreshold = self.cleaned_data["notifyThreshold"])

class RequestEmailConfirmForm(forms.Form):
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Username'}))

    def is_valid(self):
        baseValid = super().is_valid()
        queryUser = None
        try:
            queryUser = User.objects.get(username=self.cleaned_data["username"])
        except:
            self.add_error(field="username", error="The username you entered does not exist")
            baseValid = False
        return baseValid


    def save(self):
        return User.objects.get(username=self.cleaned_data["username"])

class AddTAForm(forms.Form):
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Username'}))

    def __init__(self, *args, **kwargs):
        self.lid = kwargs.pop('lid', None)
        super(AddTAForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        baseValid = super().is_valid()
        #Check if user exists
        queryUser = None
        try:
            queryUser = User.objects.get(username=self.cleaned_data["username"])
        except:
            self.add_error(field="username", error="The username you entered does not exist")
            baseValid = False
        #Check if user already has a role in the lab
        queryRole = None
        try:
            queryRole = Role.objects.get(uid_id=queryUser.id, lid_id=self.lid)
            self.add_error(field="username", error="The user is already a member of the lab")
            baseValid = False
        except:
            pass
        return baseValid

    def save(self):
        user = User.objects.get(username=self.cleaned_data["username"])
        newRole = Role(uid_id=user.id, lid_id=self.lid, role = 't')
        newRole.save()

class ContactForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

    firstName = forms.CharField(required=True, max_length=254,
                                widget=forms.TextInput({
                                    'class':'form-control',
                                    'placeholder':'First Name'}))
    lastName = forms.CharField(required=True, max_length=254,
                                widget=forms.TextInput({
                                    'class':'form-control',
                                    'placeholder':'Last Name'}))
    email = forms.EmailField(required=True,
                                widget=forms.TextInput({
                                    'class':'form-control',
                                    'placeholder':'Email'}))

    phoneNumber = forms.CharField(required=False, max_length=16,
                                widget=forms.TextInput({
                                    'class':'form-control',
                                    'placeholder':'Phone Number'}))

    message = forms.CharField(required=True, max_length=254,
                                widget=forms.Textarea({
                                    'class':'form-control',
                                    'placeholder':'Message',
                                    'rows': 8,
                                    'cols': 10 }))

    # CAPTCHA field
    captcha = CaptchaField()

    def is_valid(self):
        baseValid = super().is_valid()
        return baseValid

    def save(self):
        firstName = self.cleaned_data["firstName"]
        lastName = self.cleaned_data["lastName"]
        email = self.cleaned_data["email"]
        phoneNumber = self.cleaned_data["phoneNumber"]
        message = self.cleaned_data["message"]
