#Copyright 2019 LabLineup
#NOTE: The API Key is hardcoded and should be removed if the code is publicly published

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def sendNotification(email, labName, numRequests):
    message = Mail(
        from_email='no-reply@lablineup.com',
        to_emails=email,
        subject=("LabLineup Notification: " + labName + " has " + str(numRequests) + " requests in the queue"),
        html_content=('<h1>LabLineup Notification</h1><br><br>'+ labName + " has " + str(numRequests) + " requests in the queue."))
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
