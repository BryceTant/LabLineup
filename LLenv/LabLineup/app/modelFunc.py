from app.models import Lab
from app.models import Role
from app.models import Request
from app.models import LabCode
from django.contrib.auth.models import User
from string import ascii_lowercase
from random import choice
from random import randint


#Generates and saves a LabCode for the specified lab and role and returns the code
def generateLabCode(labID, role):
	roleList=['s', 't', 'p']
	codeString = str(labID)
	for i in range(0,5):
		charChoice = choice(ascii_lowercase)
		while charChoice in roleList:
			charChoice = choice(ascii_lowercase)
		codeString = codeString + charChoice
	newCodeString = codeString.replace(codeString[len(str(labID)) + randint(0,4)], role)
	newCode = LabCode(lid_id=labID, role=role, code=newCodeString)
	return newCode.code


#To get the role of a userID in a labID
def getRole(userID, labID):
	return Role.objects.get(uid_id=userID, lid_id=labID).role

#To get a list of labs in which the userID has role role
def getLabsWithRole(userID, role):
	labs = []
	for lidOjb in Role.objects.filter(uid_id=userID, role=role):
		labs.append(Lab.objects.get(lid=lidObj.lid_id))
	return labs

#To get a list of feedback (ratings) for a TA or professor in a lab
def getFeedbackForUser(userID, labID):
	feedback = []
	for entry in Request.objects.filter(huid_id=userID, lid_id=labID):
		feedback.append(entry.feedback)
	return feedback

#To get a list of the current requests (as a list of Request objects) in a lab
def getRequests(labID):
	requests = []
	for request in Request.objects.filter(lid_id=labID, timeCompleted__isnull=True):
		requests.append(request)
	return requests

#To get a list of completed requests for a lab (as a list of Request objects)
def getCompletedRequests(labID):
	requests = []
	for request in Request.objects.filter(lid_id=labID, timeCompleted__isnull=False):
		requests.append(request)
	return requests

#To get a list of all users in a lab (as a list of tuples containing (UserObject, role)
def getLabUsers(labID):
	users = []
	for user in Role.objects.filter(lid_id=labID):
		users.append((User.objects.get(id=user.uid_id), user.role))
	return users

#To get a list of all users in a lab with role role (as a list of user objects)
def getLabUsersWithRole(labID, role):
	users = []
	for user in Role.objects.filter(lid_id=labID, role=role).uid_id:
		users.append(User.objects.get(id=user))
	return users