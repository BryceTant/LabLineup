from app.models import Lab
from app.models import Role
from app.models import Request
from app.models import LabCode
from app.models import Notify
from app.models import PasswordResetCode
from django.contrib.auth.models import User
from string import ascii_lowercase
from string import ascii_letters
from string import digits
from random import choice
from random import randint
from django.db.models import Avg
import datetime
from statistics import mean


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
    newCode.save()
    return newCode.code

#To delete a labCode (so users can no longer use it to add the lab)
def deleteLabCode(labCode):
    LabCode.objects.filter(code=labCode).delete()

#To get lab codes for lab labID with role role
def getLabCode(labID, role):
    query = None
    try:
        query = LabCode.objects.get(lid_id=labID, role=role).code
    except:
        pass
    return query

#To get the role of a userID in a labID
def getRole(userID, labID):
    query = Role.objects.get(uid_id=userID, lid_id=labID)
    if query:
        return query.role
    else:
        return None

#To get a list of labs in which the userID has role role
def getLabsWithRole(userID, role):
    labs = []
    query = Role.objects.filter(uid_id=userID, role=role)
    if query:
        for lidObj in query:
            labs.append(Lab.objects.get(lid=lidObj.lid_id))
    return labs

#To get a list of feedback (ratings) for a TA or professor in a lab
def getFeedbackForUser(userID, labID):
    feedback = []
    query = Request.objects.filter(huid_id=userID, lid_id=labID)
    if query:
        for entry in query:
            feedback.append(entry.feedback)
    return feedback

#To get a list of the current requests (as a list of Request objects) in a lab
def getRequests(labID):
    requests = []
    query = Request.objects.filter(lid_id=labID, timeCompleted__isnull=True)
    if query:
        for request in query:
            requests.append(request)
    return requests

#To get a count of current requests in a lab
def getRequestCount(labID):
    count = Request.objects.filter(lid_id=labID, timeCompleted__isnull=True).count()
    return count

#To get a list of completed requests for a lab (as a list of Request objects)
def getCompletedRequests(labID):
    requests = []
    query = Request.objects.filter(lid_id=labID, timeCompleted__isnull=False)
    if query:
        for request in query:
            requests.append(request)
    return requests

#To get the oldest request in the queue
def getNextRequest(labID):
    return Request.objects.filter(lid_id=labID).latest('timeSubmitted')

#To get the most recent request in the queue
def getLastRequest(labID):
    return Request.objects.filter(lid_id=labID).earliest('timeSubmitted')

#To get a list of all users in a lab (as a list of tuples containing (UserObject, role)
def getLabUsers(labID):
    users = []
    query = Role.objects.filter(lid_id=labID)
    if query:
        for user in query:
            users.append((User.objects.get(id=user.uid_id), user.role))
    return users

#To get a list of all users in a lab with role role (as a list of user objects)
def getLabUsersWithRole(labID, role):
    users = []
    query = Role.objects.filter(lid_id=labID, role=role)
    if query:
        for user in query:
            users.append(User.objects.get(id=user.uid_id))
    return users

#To get a list of users to email when a new request is submitted in lab labID
def getEmailsToNotifyNew(labID):
    users = []
    queryUsers = Notify.objects.filter(lid_id = labID, notifyNew=True)
    if queryUsers:
        for user in queryUsers:
            users.append(User.objects.get(id=user.uid_id))
    return users

#To get a list of users to email when the number of requests is currentCount in lab labID
def getEmailsToNotifyThreshold(labID, currentCount):
    users = []
    queryUsers = Notify.objects.filter(notifyThreshold <= currentCount, lid_id = labID)
    if queryUsers:
        for user in queryUsers:
            users.append(User.objects.get(id=user.uid_id))
    return users

#To get the average wait time as a string of minutes:seconds for a lab
def getAvgWait(labID):
    waitTimes = []
    avgWaitTime = []
    query = Request.objects.filter(lid_id=labID)
    if query:
        for request in query:
            timeCompleted = 0
            if request.timeCompleted != None:
                #If the request has been completed
                timeCompleted = request.timeCompleted
            else:
                #If the request has not been completed, use current time
                timeCompleted = datetime.datetime.now()
            timeSubmitted = request.timeSubmitted
            timeTaken = (timeCompleted - timeSubmitted).seconds
            waitTimes.append(timeTaken)
        avgWaitTime = divmod(mean(waitTimes), 60)
    else:
        avgWaitTime = [0,0]
    return str(avgWaitTime[0]) + ":" + str(round(avgWaitTime[1],2)) #returns minutes:seconds


#To get the average wait time as a string of minutes:seconds for a lab for a specific helper
def getAvgWaitTA(labID, helperID):
    waitTimes = []
    avgWaitTime = []
    query = Request.objects.filter(lid_id=labID, huid_id=helperID)
    if query:
        for request in query:
            timeCompleted = 0
            if request.timeCompleted != None:
                #If the request has been completed
                timeCompleted = request.timeCompleted
            else:
                #If the request has not been completed, use current time
                timeCompleted = datetime.datetime.now()
            timeSubmitted = request.timeSubmitted
            timeTaken = (timeCompleted - timeSubmitted).seconds
            waitTimes.append(timeTaken)
        avgWaitTime = divmod(mean(waitTimes), 60)
    else:
        avgWaitTime = [0,0]
    return str(avgWaitTime[0]) + ":" + str(round(avgWaitTime[1],2)) #returns minutes:seconds

#To get the average feedback for a lab as an int
def getAvgFeedback(labID):
    feedbacks = []
    avgFeedback = 0
    query = Request.objects.filter(lid_id=labID).exclude(feedback=None)
    if query:
        for request in query:
            feedbacks.append(request.feedback)
        avgFeedback = mean(feedbacks)
    return avgFeedback

#To get the average feedback for a lab for a helper as an int
def getAvgFeedbackTA(labID, helperID):
    feedbacks = []
    avgFeedback = 0
    query = Request.objects.filter(lid_id=labID, huid_id=helperID).exclude(feedback=None)
    if query:
        for request in query:
            feedbacks.append(request.feedback)
        avgFeedback = mean(feedbacks)
    return avgFeedback

#To get the number of requests completed for a lab
def getNumComplete(labID):
    queryCount = Request.objects.filter(lid_id=labID).exclude(timeCompleted=None).count()
    return queryCount

#To get the number of requests a helper has completed for a lab
def getNumCompleteTA(labID, helperID):
    queryCount = Request.objects.filter(lid_id=labID, huid_id=helperID).exclude(timeCompleted=None).count()
    return queryCount

#To delete a lab (and all related data). This action should be confirmed beforehand
def deleteLab(labID):
    #Delete all requests
    Request.objects.filter(lid_id=labID).delete()
    #Delete all users' roles
    Role.objects.filter(lid_id=labID).delete()
    #Delete all lab codes
    LabCode.objects.filter(lid_id=labID).delete()
    #Delete all notification settings
    Notify.objects.filter(lid_id=labID).delete()
    #Delete lab
    Lab.objects.filter(lid=labID).delete()

#To get a user object by searching by email
def getUserByEmail(emailAddr):
    query = None
    try:
        query = User.objects.get(email=emailAddr)
    except:
        pass
    return query

#To generate a random alphanumeric string of specified length
#Taken from PYNative (https://pynative.com/python-generate-random-string/)
def randomAlphanumericString(length=25):
    lettersAndNumbers = ascii_letters + digits
    return ''.join(choice(lettersAndNumbers) for i in range(length))

#To generate a password reset code
def generatePasswordResetCode(userID):
    prcSet = False
    while not prcSet:
        try:
            newPRC = PasswordResetCode(uid_id=userID, prc=randomAlphanumericString(length=25), timeGenerated=datetime.datetime.now())
            newPRC.save()
            prcSet = True
            return newPRC
        except:
            pass

#To reset the password
def resetPasswordFunc(prc, newPassword):
    query = None
    try:
        query = PasswordResetCode.objects.get(prc=prc)
    except:
        return False #Return False if unsuccessful
    user = User.objects.get(id=query.uid_id)
    user.set_password(newPassword)
    user.save()
    query.delete()
    return True #Return True if successful

#To get the user's notifications settings object for the specified lab
def getNotificationSettings(userID, labID):
    query = None
    try:
        query = Notify.objects.get(uid_id = userID, lid_id = labID)
    except:
        pass
    return query