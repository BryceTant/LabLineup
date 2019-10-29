#Copyright 2019 LabLineup
#NOTE: The API Key is hardcoded and should be removed if the code is publicly published

import requests

API='https://api.mailgun.net/v3/sandbox5cabdfbc85c04547bc9022f1756f244f.mailgun.org/messages'
API_KEY='8417d7db91e6ff4430906312affaf067-816b23ef-53a937ca'

def sendNotification(email, labName, numRequests):
    message={}
    message["from"] = "LabLineup <no-reply@lablineup.com>"
    message["to"] = [email]
    message["subject"] = ("LabLineup Alert for " + labName)
    message["text"] = (labName + " has " + str(numRequests) + " requests in the queue.")
    return requests.post(API,auth=('api',API_KEY),data=message)
