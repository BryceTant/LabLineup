from app.models import Lab
from app.models import Role
from app.models import Request
from app.models import LabCode
from app.models import Notify
from app.models import PasswordResetCode
from app.models import Subscription
from app.models import EmailConfirmation
from django.contrib.auth.models import User
from string import ascii_lowercase
from string import ascii_letters
from string import digits
from random import choice
from random import randint
from django.db.models import Avg
import datetime
from statistics import mean
from pytz import utc as utc
from django.utils import timezone
from dateutil.relativedelta import relativedelta


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

#To get the number of labs in which the user is a professor (owner)
def getNumberOfLabs(userID):
    return Role.objects.filter(uid_id=userID, role='p').count()

#To get a user's lab limit (as professor/owner)
def getLabLimit(userID):
    query = None
    try:
        query = Subscription.objects.get(uid_id=userID).labLimit
    except:
        pass
    return query

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

#To get the oldest request in the queue with no helper assigned
def getNextRequest(labID):
    return Request.objects.filter(lid_id=labID, timeCompleted=None).earliest('timeSubmitted')

#To get the most recent request in the queue
def getLastRequest(labID):
    return Request.objects.filter(lid_id=labID).latest('timeSubmitted')

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
    queryUsers = Notify.objects.filter(notifyThreshold = currentCount, lid_id = labID)
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
                timeCompleted = datetime.datetime.now(utc)
            timeSubmitted = request.timeSubmitted
            timeTaken = (timeCompleted - timeSubmitted).seconds
            waitTimes.append(timeTaken)
        avgWaitTime = divmod(mean(waitTimes), 60)
    else:
        avgWaitTime = [0,0]
    return str(int(avgWaitTime[0])) + ":" + str(int(round(avgWaitTime[1],0))) #returns minutes:seconds


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
                timeCompleted = datetime.datetime.now(utc)
            timeSubmitted = request.timeSubmitted
            timeTaken = (timeCompleted - timeSubmitted).seconds
            waitTimes.append(timeTaken)
        avgWaitTime = divmod(mean(waitTimes), 60)
    else:
        avgWaitTime = [0,0]
    return str(int(avgWaitTime[0])) + ":" + str(int(round(avgWaitTime[1],0))) #returns minutes:seconds

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

#To generate a registration confirmation code
def generateRegConCode(userID):
    regConCodeSet = False
    while not regConCodeSet:
        try:
            newRCC = EmailConfirmation(uid_id=userID,
                                       regConCode=randomAlphanumericString(length=25))
            newRCC.save()
            regConCodeSet = True
            return newRCC
        except:
            pass

#To confirm an account using a registration confirmation code
def confirmAccount(regConCode):
    query = None
    try:
        query = EmailConfirmation.objects.get(regConCode=regConCode)
    except:
        pass
    if query == None:
        #The given confirmation code does not exist
        return False
    else:
        #If the given confirmation code is found, activate the account
        user = User.objects.get(id=query.uid_id)
        user.is_active = True
        user.save()
        #Delete the regConCode, as it is no longer needed
        query.delete()
        return True

#To get the first a last name of a user
def getNameOfUser(userID):
    query = None
    name = ""
    try:
        query = User.objects.get(id=userID)
        name = query.first_name + " " + query.last_name
    except:
        pass
    if (query != None):
        return name
    else:
        return None

#To get an open request for a student for a lab (for the student view)
def getStudentCurrentRequest(labID, userID):
    query = None
    try:
        query = Request.objects.get(lid_id = labID, suid_id=userID, timeCompleted=None)
    except:
        pass
    return query

#To get a request that is assigned but not completed in a lab
def getOutstandingRequest(labID, userID):
    query = None
    try:
        query = Request.objects.get(lid_id=labID, huid_id=userID, complete=False)
    except:
        pass
    return query

#To get the number of requests that are assigned but not completed in a lab for a specific helper
def getNumOutstandingRequestsTA(labID, helperID):
    queryCount = Request.objects.filter(lid_id=labID, 
                                        huid_id=helperID, 
                                        complete=False, 
                                        timeCompleted=None).count()
    return queryCount

#To remove a lab from an account (remove the role)
def removeLabFromAccount(userID, labID):
    query = None
    try:
        query = Role.objects.get(uid_id=userID, lid_id=labID)
    except:
        pass
    if query != None:
        query.delete()
        return True
    else:
        return False

#To set a lab to inactive (when a professor deletes the lab or their account)
def setLabInactive(labID):
    query = None
    successful = False
    try:
        query = Lab.objects.filter(lid=labID)
        query.update(active=False)
        query
        successful = True
    except:
        pass
    return successful

#To delete an account (actually, deactivates)
def deleteAccount(userID):
    #Find account
    queryAccount = None
    try:
        queryAccount = User.objects.filter(id=userID)
    except:
        return (False, "The account was not found")
    #Set owned labs to inactive
    labsOwned = getLabsWithRole(userID=userID, role='p')
    for lab in labsOwned:
        Lab.objects.filter(lid=lab.lid).update(active=False)
    #Delete roles
    queryRoles = None
    try:
        queryRoles = Role.objects.filter(uid_id=userID).delete()
    except:
        pass
    #Delete notification settings
    queryNotify = None
    try:
        queryNotify = Notify.objects.filter(uid_id=userID).delete()
    except:
        pass #No notification settings set
    #Delete password reset codes
    queryPRC = None
    try:
        queryPRC = PasswordResetCode.objects.filter(uid_id=userID).delete()
    except:
        pass
    querySub = None
    try:
        querySub = Subscription.objects.filter(uid_id=userID).delete()
    except:
        pass
    queryEmailConf = None
    try:
        queryEmailConf = EmailConfirmation.objects.filter(uid_id=userID).delete()
    except:
        pass
    #Deactivate account
    try:
        queryAccount.update(email="None", is_active=False)
    except:
        return (False, "The account could not be deleted")
    return True

#To get list of requests as dictionary for student for lab for requestHistory
def getStudentRequestsHistory(userID, labID):
    retList = []
    queryRequests = None
    try:
        queryRequests = Request.objects.filter(suid_id=userID, lid_id=labID).order_by('-timeSubmitted')
        for request in queryRequests:
            genDict = {"timeSubmitted":request.timeSubmitted,
                       "timeCompleted":request.timeCompleted,
                       "station":request.station,
                       "description":request.description,
                       "help":getNameOfUser(request.huid_id),
                       "feedback":request.feedback
                      }
            retList.append(genDict)
    except:
        pass
    return retList

#To get requestHistory
def getRequestHistory(userID):
    retDict = {}
    listLabs = getLabsWithRole(userID, 's')
    for lab in listLabs:
        retDict[lab.name] = getStudentRequestsHistory(userID, labID=lab.lid)
    return retDict

#To convert UTC to local datetime
def convertToLocal(utctime):
    """This function copied from https://stackoverflow.com/questions/26812805/django-convert-utc-to-local-time-zone-in-views Created by: Stack Overflow User jakobdo"""
    fmt = '%d/%m/%Y %H:%M'
    utc = utctime.replace(tzinfo=pytz.UTC)
    localtz = utc.astimezone(timezone.get_current_timezone())
    return localtz.strftime(fmt)

#To update a user's subscription
def updateUserSub(userID, plan):
    """Yearly Plans: 0=Free, 1=Silver, 2=gold"""
    planLimits = {0:1, 1:5, 2:20}
    query = None
    try:
        query = Subscription.objects.filter(uid_id=userID)
    except:
        return False
    query = query[0]
    now = datetime.datetime.now(utc)
    initialSub = query.initialSub
    subRenewal = query.subRenewal
    if query.labLimit == 1:
        #This is a new premium subscription
        initialSub = now
        subRenewal = now
    renewDate = subRenewal + relativedelta(years=1) # Add 1 year
    Subscription.objects.filter(uid_id=userID).update(initialSub = initialSub,
                                                      lastSub = now,
                                                      subRenewal = renewDate,
                                                      labLimit = planLimits[plan]
                                                      )
    return True

#To update a user's subcription 
def updateSub(subID, plan):
    """Yearly Plans: 0=Free, 1=Silver, 2=gold"""
    planLimits = {0:1, 1:5, 2:20}
    query = None
    try:
        query = Subscription.objects.filter(id=subID)
    except:
        return False
    query = query[0]
    now = datetime.datetime.now(utc)
    initialSub = query.initialSub
    subRenewal = query.subRenewal
    if query.labLimit == 1:
        #This is a new premium subscription
        initialSub = now
        subRenewal = now
    renewDate = subRenewal + relativedelta(years=1) # Add 1 year
    Subscription.objects.filter(id=subID).update(initialSub = initialSub,
                                                      lastSub = now,
                                                      subRenewal = renewDate,
                                                      labLimit = planLimits[plan]
                                                      )
    return True

#To update a user's sub's orderID
def updateSubOrder(subID, orderID):
    query = None
    try:
        query = Subscription.objects.filter(id=subID).update(orderID=orderID)
    except:
        return False
    return True

#To confirm that an orderID has not already been used
def confirmNewSub(subID, orderID):
    query = None
    try:
        query = Subscription.objects.get(id=subID)
        if orderID != query.orderID:
            return True
        else:
            return False
    except:
        return False

#To get a user's subscription
def getSub(userID):
    query = None
    try:
        query = Subscription.objects.get(uid_id=userID)
    except:
        pass
    return query

#To update a request's feedback
def updateFeedback(rid, feedback):
    query = None
    try:
        query = Request.objects.filter(rid=rid).update(feedback = feedback)
        query.save()
        return True
    except:
        return False

#To cancel a request        
def cancelRequest(req):
    query = None
    try:
        query = Request.objects.get(rid = req.rid)
    except:
        pass
    if query != None:
        query.delete()
        return True
    else:
        return False
 
#To mark a request as complete by adding a timeCompleted
def markRequestComplete(rid):
    query = None
    now = datetime.datetime.now(utc)
    try:
        query = Request.objects.filter(rid=rid).update(timeCompleted=now, complete=True)
        return True
    except:
        return False

#To mark a request not complete but set timeCompleted
def markRequestNotComplete(rid):
    query = None
    now = datetime.datetime.now(utc)
    try:
        query = Request.objects.filter(rid=rid).update(timeCompleted=now, complete=False)
        return True
    except:
        return False