#Copyright 2019 LabLineup
#NOTE: The API Key is hardcoded and should be removed if the code is publicly published

from app.modelFunc import getEmailsToNotifyNew
from app.modelFunc import getEmailsToNotifyThreshold
from app.modelFunc import getLastRequest

from app.models import Lab
from app.models import Request
from django.contrib.auth.models import User

import requests


API='https://api.mailgun.net/v3/notify.lablineup.com/messages'
API_KEY='8417d7db91e6ff4430906312affaf067-816b23ef-53a937ca'
FROM = "LabLineup <no-reply@lablineup.com>"

def sendEmail(emails, subject, text):
	"""Takes in list of emails"""
	message={}
	message["from"] = FROM
	message["to"] = emails
	message["subject"] = subject
	message["html"] = text
	return requests.post(API,auth=('api',API_KEY),data=message)


def sendNewRequest(lid):
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

	sendEmail(getEmailsToNotifyNew(lid), subject, text)

def sendThreshold(lid, currentCount):
	labName = Lab.objects.get(lid=lid).name
	subject = labName + " currently has " + str(currentCount) + " requests"

	text = "LabLineup currently has " + str(currentCount) + " requests in the queue."
	text = text + "\nThis exceeds your threshold."

	#getEmailsToNotifyThreshold could return null. That should prevent the message from sending
	sendEmail(getEmailsToNotifyThreshold(lid, currentCount), subject, text)

def sendAllRequest(lid, currentCount):
	sendNewRequest(lid)
	sendThreshold(lid, currentCount)

def sendPasswordReset(user, prc):
    baseURL = '127.0.0.1:8000'
    resetLink = "<a href=" + baseURL + "/account/resetPassword/"+ str(prc) + ">"
    resetLink = resetLink + baseURL + "/account/resetPassword/" + str(prc) + "</a>"
    text = "A password reset link has been requested for your account. <br>"
    text = text + "Your username is " + str(user.username) + "<br>"
    text = text + "Go to " + resetLink + " to reset your password."
    sendEmail([user.email], "Password Reset Link", text)