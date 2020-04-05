#Copyright 2020 LabLineup

from app.modelFunc import getLabsWithOpen


def getRequestAlert(userID):
    labs = getLabsWithOpen(userID)
    if len(labs) > 0:
        title = "Help Requested"
        message = ""
        for labName in labs:
            message = message + labName + ", "
        message = message[:-2]
        if len(labs) > 1:
            message = message + " have"
        else:
            message = message + " has"
        message = message + " one or more students requesting help."
        return (title, message)
    else:
        return None

def getAlerts(userID):
    alerts = []
    requestAlert = getRequestAlert(userID)
    if requestAlert != None:
        alerts.append(requestAlert)
    return alerts