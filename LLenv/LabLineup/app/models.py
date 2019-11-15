"""
Definition of models.
"""

from django.db import models
from django.conf.global_settings import AUTH_USER_MODEL

class Lab(models.Model):
	lid = models.AutoField(primary_key=True)  #int(11), ~Null, PK, auto_inc
	name = models.CharField(max_length=75)  #varchar(75), ~Null
	description = models.CharField(max_length=150)  #varchar(150), ~Null


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
