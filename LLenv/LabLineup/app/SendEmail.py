#Copyright 2019 LabLineup
#NOTE: The API Key is hardcoded and should be removed if the code is publicly published

from app.modelFunc import getEmailsToNotifyNew
from app.modelFunc import getEmailsToNotifyThreshold
from app.modelFunc import getLastRequest

from app.models import Lab
from app.models import Request
from django.contrib.auth.models import User

import requests  #Note: this is for HTTP requests, not lab requests
from datetime import datetime


API='https://api.mailgun.net/v3/notify.lablineup.com/messages'
API_KEY='8417d7db91e6ff4430906312affaf067-816b23ef-53a937ca'
FROM = "LabLineup <no-reply@lablineup.com>"
BASEURL = '127.0.0.1:8000'

def sendEmailPlaintext(emails, subject, text):
    """Takes in list of emails, a subject, and text and sends the email"""
    message={}
    message["from"] = FROM
    message["to"] = emails
    message["subject"] = subject
    message["text"] = text
    return requests.post(API,auth=('api',API_KEY),data=message)

def sendEmail(emails, subject, template, variables):
    """Takes in list of emails"""
    message={}
    message["from"] = FROM
    message["to"] = emails
    message["subject"] = subject
    message["template"] = template
    message["h:X-Mailgun-Variables"] = variables
    return requests.post(API,auth=('api',API_KEY),data=message)


def sendNewRequestPlaintext(lid):
    labName = Lab.objects.get(lid=lid).name
    subject = labName + " has received a new request"
    request = getLastRequest(lid)
    studentName = User.objects.get(id=request.uid_id).first_name + " " + User.objects.get(id=request.uid_id).last_name

    text = "LabLineup has received a new request"
    text = text + "\n REQUEST:\n"
    text = text + "Student:\t" + studentName + "\n"
    text = text + "Station:\t" + request.station + "\n"
    text = text + "Submitted:\t" + str(request.timeSubmitted) + "\n"
    text = text + "Description:\t" + str(request.description)

    sendEmailPlaintext(getEmailsToNotifyNew(lid), subject, text)

def sendThresholdPlaintext(lid, currentCount):
    labName = Lab.objects.get(lid=lid).name
    subject = labName + " currently has " + str(currentCount) + " requests"

    text = "LabLineup currently has " + str(currentCount) + " requests in the queue."
    text = text + "\nThis exceeds your threshold."

    #getEmailsToNotifyThreshold could return null. That should prevent the message from sending
    sendEmailPlaintext(getEmailsToNotifyThreshold(lid, currentCount), subject, text)

def sendAllRequest(lid, currentCount):
    sendNewRequest(lid)
    sendThreshold(lid, currentCount)

def sendPasswordReset(user, prc):
    """Takes a user object and prc code and send the password reset link"""
    resetLink = BASEURL + "/account/resetPassword/" + str(prc)
    vars = "{\"prcLink\": \"" + resetLink + "\", \"username\": \"" + str(user.username) + "\"}"
    sendEmail([user.email], "Password Reset Link", template="passwordreset", variables=vars)

def sendNewRequest(lid):
    labName = Lab.objects.get(lid=lid).name
    subject = labName + " has received a new request"
    request = getLastRequest(lid)
    student = User.objects.get(id=request.suid_id)
    studentName = student.first_name + " " + student.last_name
    dateSubmitted = request.timeSubmitted.strftime("%m/%d/%Y %I:%M:%S %p")

    vars = "{\"labName\": \"" + labName + "\","
    vars = vars + "\"student\": \"" + studentName + "\","
    vars = vars + "\"station\": \"" + request.station + "\","
    vars = vars + "\"submitted\": \"" + dateSubmitted + "\","
    vars = vars + "\"description\": \"" + request.description + "\","
    vars = vars + "\"labLink\": \"" + BASEURL + "\"}"

    sendEmail(getEmailsToNotifyNew(lid), subject, template="newrequest", variables=vars)

def sendThreshold(lid, currentCount):
    labName = Lab.objects.get(lid=lid).name
    subject = labName + " currently has " + str(currentCount) + " requests"

    vars = "{\"labName\": \"" + labName + "\","
    vars = vars + "\"numRequests\": \"" + str(currentCount) + "\","
    vars = vars + "\"labLink\": \"" + BASEURL + "\"}"

    sendEmail(getEmailsToNotifyThreshold(lid, currentCount), subject, template="thresholdrequest", variables=vars)

def sendRegistrationConfirmation(user, regConCode):
    subject = "LabLineup Account Confirmation"
    regConLink = BASEURL + "/account/confirmAccount/" + str(regConCode)

    vars = "{\"firstName\": \"" + user.first_name + "\","
    vars = vars + "\"regConLink\": \"" + regConLink + "\"}"

    sendEmail([user.email], subject, template="accountconfirm", variables=vars)

def sendNeverHelped():
    profEmail = "Get professor email for this"
    subject = "A student was NOT helped in " + labName
    labName = Lab.objects.get(lid=lid).name
    studentName = student.first_name + " " + student.last_name
    station = None
    dateSubmitted = request.timeSubmitted.strftime("%m/%d/%Y %I:%M:%S %p")
    description = None
    helperName = "TAFirst TA Last"

    vars = "{\"labName\": \"" + labName + "\","
    vars = vars + "\"student\": \"" + studentName + "\","
    vars = vars + "\"station\": \"" + station + "\","
    vars = vars + "\"submitted\": \"" + dateSubmitted + "\","
    vars = vars + "\"description\": \"" + description + "\","
    vars = vars + "\"helper\": \"" + helperName + "\","
    vars = vars + "\"labLink\": \"" + BASEURL + "\"}"

    sendEmail(profEmail, subject, template="nothelped", variables=vars)