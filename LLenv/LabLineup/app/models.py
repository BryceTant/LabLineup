"""
Definition of models.
"""

from django.db import models
from django.conf.global_settings import AUTH_USER_MODEL

class Lab(models.Model):
    lid = models.AutoField(primary_key=True)  #int(11), ~Null, PK, auto_inc
    name = models.CharField(max_length=75)  #varchar(75), ~Null
    description = models.CharField(max_length=150)  #varchar(150), ~Null
    active = models.BooleanField(default=True) # bool


class Role(models.Model):
	lid = models.ForeignKey('Lab',on_delete=models.CASCADE)  #int(11), ~Null, FK
	uid = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)  #int(11), ~Null, FK
	RoleChoices = (('s',"Student"), ('p', "Professor"), ('t', "Teaching Assistant"))
	role = models.CharField(max_length=1, choices=RoleChoices, default='s')  #varchar(1) (choice)


class Request(models.Model):
	rid = models.AutoField(primary_key=True) #int(11), ~Null, PK, auto_inc
	station = models.CharField(max_length=10)  #varchar(11), ~Null
	description = models.CharField(max_length=250)  #varchar(250), ~Null
	timeSubmitted = models.DateTimeField() #datetime, ~Null
	timeCompleted = models.DateTimeField(null=True, blank=True)  #datimee, NULL
	feedback = models.IntegerField(null=True, blank=True)  #int(1), NULL
	suid = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="suid")  #int(11), ~Null, FK
	lid = models.ForeignKey('Lab', on_delete=models.CASCADE)  #int(11), ~Null, FK
	huid = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="huid", null=True)  #int(11), Null, FK


class LabCode(models.Model):
	code = models.CharField(max_length=20, primary_key=True, unique=True)
	lid = models.ForeignKey('Lab', on_delete=models.CASCADE)
	RoleChoices = (('s',"Student"), ('p', "Professor"), ('t', "Teaching Assistant"))
	role = models.CharField(max_length=1, choices=RoleChoices, default='s')  #varchar(1) (choice)

class Notify(models.Model):
	uid = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE) #int(11)
	lid = models.ForeignKey('Lab', on_delete=models.CASCADE)
	notifyNew = models.BooleanField(default=False)
	notifyThreshold = models.IntegerField(null=True, blank=True)

class PasswordResetCode(models.Model):
	uid = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE) #int(11)
	prc = models.CharField(primary_key=True, max_length=25) #varchar(25) ~Null
	timeGenerated = models.DateTimeField()

class Subscription(models.Model):
    uid = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE) #int(11)
    initialSub = models.DateTimeField(null=True, blank=True)
    lastSub = models.DateTimeField(null=True, blank=True)
    subRenewal = models.DateTimeField(null=True, blank=True)
    labLimit = models.IntegerField()
    orderID = models.CharField(max_length=40, null=True, default=None)

class EmailConfirmation(models.Model):
    uid = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE) #int(11)
    regConCode = models.CharField(primary_key=True, max_length=25) #varchar(25)