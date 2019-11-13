"""
Definition of models.
"""

from django.db import models
#from django.conf.global_settings import AUTH_USER_MODEL

class TestTable:
	testid = models.AutoField(primary_key=True)  #int(11), ~Null, PK, auto_inc
	name_test = models.CharField(max_length=20)  #varchar(75), ~Null
	description_test = models.CharField(max_length=100)  #varchar(150), ~Null

#class Lab:
#	lid = models.AutoField(primary_key=True)  #int(11), ~Null, PK, auto_inc
#	name = models.CharField(max_length=75)  #varchar(75), ~Null
#	description = models.CharField(max_length=150)  #varchar(150), ~Null


#class Role:
#	lid = models.ForeignKey('Lab',on_delete=models.CASCADE)  #int(11), ~Null, FK
#	uid = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)  #int(11), ~Null, FK
#	RoleChoices = (('s',"Student"), ('p', "Professor"), ('t', "Teaching Assistant"))
#	role = models.CharField(max_length=1, choices=RoleChoices, default='s')  #varchar(1) (choice)


#class Request:
#	rid = models.AutoField(primary_key=True) #int(11), ~Null, PK, auto_inc
#	station = models.CharField(max_length=10)  #varchar(11), ~Null
#	description = models.CharField(max_length=250)  #varchar(250), ~Null
#	timeSubmitted = models.DateTimeField() #datetime, ~Null
#	timeCompleted = models.DateTimeField(blank=True)  #datimee, NULL
#	feedback = models.IntegerField(max_length=1, blank=True)  #int(1), NULL
#	suid = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)  #int(11), ~Null, FK
#	lid = models.ForeignKey('Lab', on_delete=models.CASCADE)  #int(11), ~Null, FK
#	huid = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)  #int(11), ~Null, FK


# Create your models here.
