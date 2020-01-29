"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.views.generic import CreateView
from django.contrib.auth import update_session_auth_hash
from pytz import utc as utc

from app.forms import BootstrapRegisterForm
from app.forms import AddLabForm
from app.forms import CreateLabForm
from app.forms import ManageLabForm
from app.forms import SubmitRequestForm
from app.forms import ChangePasswordForm
from app.forms import EditAccountDetailsForm
from app.forms import ResetPasswordForm
from app.forms import ForgotPasswordForm
from app.forms import ManageLabNotificationsForm
from app.forms import RequestEmailConfirmForm
from app.forms import AddTAForm

from app.models import Lab
from app.models import Role
from app.models import Request
from app.models import LabCode
from app.models import Notify
from app.models import Subscription
from app.models import EmailConfirmation
from app.modelFunc import generateLabCode
from app.modelFunc import getLabsWithRole
from app.modelFunc import getNumberOfLabs
from app.modelFunc import getLabLimit
from app.modelFunc import getRole
from app.modelFunc import getLabCode
from app.modelFunc import deleteLabCode
from app.modelFunc import getRequestCount
from app.modelFunc import getUserByEmail
from app.modelFunc import generatePasswordResetCode
from app.modelFunc import resetPasswordFunc
from app.modelFunc import getNotificationSettings
from app.modelFunc import generateRegConCode
from app.modelFunc import confirmAccount
from app.modelFunc import getAvgWait
from app.modelFunc import getNextRequest
from app.modelFunc import getNameOfUser
from app.modelFunc import getOutstandingRequest
from app.modelFunc import getNumOutstandingRequests
from app.modelFunc import removeLabFromAccount
from app.modelFunc import getLabUsersWithRole
from app.modelFunc import setLabInactive
from app.modelFunc import deleteAccount
from app.modelFunc import getRequestHistory
from app.modelFunc import getNumComplete
from app.modelFunc import getAvgFeedback
from app.modelFunc import getLastRequest

from app.SendEmail import sendAllRequest
from app.SendEmail import sendPasswordReset
from app.SendEmail import sendRegistrationConfirmation


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title': 'Contact Us',
            'message': 'Please feel free to contact us with any suggestions or comments.',
            'year': datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': 'About',
            'message': 'About LabLineup',
            'year': datetime.now().year,
        }
    )

def register(request):
    """Renders the register page."""
    assert(isinstance(request, HttpRequest))
    if request.method == 'POST':
        form = BootstrapRegisterForm(request.POST)
        if form.is_valid():
            output = form.save()
            rcc = generateRegConCode(output.id)
            sendRegistrationConfirmation(output, rcc.regConCode)
            return render(
                    request,
                    'app/message.html',
                    {
                        'title':"Welcome to LabLineup",
                        'message': "Please check your email for a link to activate your account.",
                        'year': datetime.now().year
                    }
                )
    else:
        form = BootstrapRegisterForm()
    return render(
        request,
        'app/register.html',
        {
            'title': 'Register',
            'message:': 'Create an account.',
            'year': datetime.now().year,
            'form': form
        }
    )

def help(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/help.html',
        {
            'title': 'FAQs',
            'message': 'Help / Frequently Asked Questions',
            'year': datetime.now().year,
        }
    )

def createLab(request):
    """Renders the createLab page. """
    assert isinstance(request, HttpRequest)
    labLimit = getLabLimit(userID=request.user)
    if (labLimit != None and getNumberOfLabs(userID=request.user) >= labLimit):
        return render(
            request,
            'app/error.html',
            {
                'title': "Error",
                'message': "You have reached your limit for labs as a professor. Please upgrade your subscription.",
                'year': datetime.now().year
            }
        )
    else:
        if request.method == 'POST':
            form = CreateLabForm(request.POST, user=request.user)
            if form.is_valid():
                newLabID = form.save()
                request.session["currentLab"] = newLabID
                return redirect('/lab/manageLab')
        else:
            form = CreateLabForm(user=request.user)
        return render(
            request,
            'app/createLab.html',
            {
                'title': 'Create Lab',
                'message': 'Create a lab for your class',
                'year': datetime.now().year,
                'form': form
            }
        )

def addLab(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = AddLabForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('/app')

    else:
        form = AddLabForm(user=request.user)
    return render(
        request,
        'app/addLab.html',
        {
            'title': 'Add Lab',
            'message': 'Add a lab to your account',
            'year': datetime.now().year,
            'form': form,
        }
    )

def selectLab(request):
    """Renders main app page (select a lab)"""
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        selectedLabID = request.POST.get("labID", None)
        selectedLabIDRemove = request.POST.get("labIDRemove", None)
        if selectedLabID != None:
            request.session["currentLab"] = selectedLabID
            role = getRole(userID=request.user, labID=selectedLabID)
            if role == 's':
                return redirect('/student/request')
            else:  # TA or professor
                return redirect('/lab/queue')
        if selectedLabIDRemove != None:
            removed = removeLabFromAccount(userID=request.user, labID=selectedLabIDRemove)
            if removed:
                # Lab removed from account
                return redirect('/app')
            else:
                return render(
                    request,
                    'app/error.html',
                    {
                        'title': "Error",
                        'message': "The lab could not be removed from your account. Please contact us.",
                        'year': datetime.now(utc).year
                    }
                )
    else:
        # Lists of lab objects for each role
        labsWhereStudent = getLabsWithRole(userID=request.user, role='s')
        labsWhereTA = getLabsWithRole(userID=request.user, role='t')
        labsWhereProfessor = getLabsWithRole(userID=request.user, role='p')
        return render(
            request,
            'app/selectLab.html',
            {
                'title': 'Select Lab',
                'message': 'Select a lab',
                'year': datetime.now(utc).year,
                'labsWhereStudent': labsWhereStudent,
                'labsWhereTA': labsWhereTA,
                'labsWhereProfessor': labsWhereProfessor
            }
        )

def studentRequest(request):
    """Renders page for student to submit request."""
    # Should only render if user's role is student
    # Blank Request Form => Request Waiting Form => Feedback Form
    assert isinstance(request, HttpRequest)
    currentLID = request.session.get('currentLab')
    if (getRole(userID=request.user, labID=currentLID) == 's'):
        if request.method == 'POST':
            form = SubmitRequestForm(
                request.POST, user=request.user, lid=currentLID)
            if form.is_valid():
                newRID = form.save()
                request.session["currentRequest"] = newRID
                sendAllRequest(currentLID, getRequestCount(currentLID))
                return redirect('/student/requestSubmitted')
        else:
            form = SubmitRequestForm(user=request.user, lid=currentLID)
        return render(
            request,
            'app/submitRequest.html',
            {
                'title': 'Submit Request',
                'message': 'Submit a request for help',
                'year': datetime.now().year,
                'form': form
            }
        )
    else:
        return render(
            request,
            'app/permissionDenied.html',
            {
                'title': 'Permission Denied',
                'message': 'You do not have permission to view this page',
                'year': datetime.now().year
            }
        )

def studentRequestSubmitted(request):
    """Renders pages for lab/{labID}/student."""
    # Blank Request Form => Request Waiting Form => Feedback Form
    assert isinstance(request, HttpRequest)
    currentLID = request.session.get('currentLab')
    avgWait = getAvgWait(currentLID)
    stationID = request.session.get('request')
    numBefore = getRequestCount(currentLID) - 1
    lab = Lab.objects.get(lid=currentLID)
    currRequest = getLastRequest(currentLID)
    # Should only render if user's role is student
    if (getRole(userID=request.user, labID=currentLID) == 's'):
        return render(
            request,
            'app/studentRequestSubmitted.html',
            {
                'title': 'Request Submitted',
                'message': 'Your request has been submitted',
                'year': datetime.now().year,
                'avgWait': avgWait,
                'stationID': currRequest.station,
                'labID': lab.name,
                'numBefore': numBefore
            }
        )
    else:
        pass

def studentRequestFeedback(request):
    """Renders pages for lab/{labID}/student."""
    # Blank Request Form => Request Waiting Form => Feedback Form
    assert isinstance(request, HttpRequest)
    currentLID = request.session.get('currentLab')
    # Should only render if user's role is student
    if (getRole(userID=request.user, labID=currentLID) == 's'):
        return render(
        request,
        'app/studentRequestFeedback.html',
        {
            'title': 'Feedback',
            'message': 'Please submit feedback about the help you received',
            'year': datetime.now().year
        }
    )
    else:
        pass

def labQueue(request):
    """Renders queue for lab (for TA's and professors)"""
    # Should only render if user's role is TA or professor
    assert isinstance(request, HttpRequest)
    currentLID = request.session.get('currentLab')
    lab = Lab.objects.get(lid=currentLID)
    role = getRole(userID=request.user, labID = currentLID)
    if (role == 'p' or role == 't'):
        #User is a prof or TA and should have access
        return render(
            request,
            'app/queue.html',
            {
                'title': lab.name,
                'message': 'Queue',
                'year': datetime.now().year,
                'role': role,
                'requestCount': str(getRequestCount(currentLID)),
                'averageWait': str(getAvgWait(currentLID))
            }
        )
    else:
        #User is a student, render access denied
        return render(
            request,
            'app/permissionDenied.html',
            {
                'title': 'Permission Denied',
                'message': 'You do not have permission to view this page',
                'year': datetime.now().year
            }
        )

def labManage(request):
    """Renders manage lab page for professors and TAs (pages will be different)"""
    # Should only render if user's role is professor
    assert isinstance(request, HttpRequest)
    currentLID = request.session.get('currentLab')
    currentLab = Lab.objects.get(lid=currentLID)
    initialData = {
        'lid': currentLID,
        'labName': currentLab.name,
        'labDescription': currentLab.description
    }
    # If the user is a professor for the current lab
    if (getRole(userID=request.user, labID=currentLID) == 'p'):
        userNotificationSettings = getNotificationSettings(userID=request.user, labID=currentLID)
        if userNotificationSettings == None:
            userNotificationSettings = Notify(uid_id=request.user.id,
                                              lid_id=currentLID,
                                              notifyNew=False,
                                              notifyThreshold=0)
            userNotificationSettings.save()
        initialData["notifyNew"] = userNotificationSettings.notifyNew
        initialData["notifyThreshold"] = userNotificationSettings.notifyThreshold
        # Load page to manage lab
        if request.method == 'POST':
            form = ManageLabForm(request.POST,
                                     prefix='detailsForm',
                                     lid=currentLID,
                                     initial=initialData)
            notificationForm = ManageLabNotificationsForm(request.POST,
                                                              user=request.user,
                                                              prefix='notificationForm',
                                                              lid=currentLID)
            studentLabCode = getLabCode(currentLID, 's')
            taLabCode = getLabCode(currentLID, 't')
            students = getLabUsersWithRole(labID=currentLID, role='s')
            tas = getLabUsersWithRole(labID=currentLID, role='t')
            addTAform = AddTAForm(request.POST, prefix='addTAForm', lid=currentLID)
            if 'detailsForm' in request.POST:  # If the lab name/description was saved
                if form.is_valid():
                    form.save()
                    return redirect('/lab/manageLab')
            elif 'notificationForm' in request.POST:  # If the notification settings were updated
                if notificationForm.is_valid():
                    notificationForm.save()
                    return redirect('/lab/manageLab')
            elif 'userIDRemove' in request.POST:  # If a user was removed
                userToRemove = request.POST.get("userIDRemove", None)
                removed = removeLabFromAccount(userID=userToRemove, labID=currentLID)
                if removed:
                    #Removed successfully
                    return redirect('/lab/manageLab')
                else:
                    return render(
                        request,
                        'app/error.html',
                        {
                            'title': "Error",
                            'message': "The user was not removed. Please contact us",
                            'year': datetime.now(utc).year
                        }
                    )
            elif 'deleteLab' in request.POST:  # If a lab was deleted
                deleteLabConfirmation = request.POST.get("deleteLab", False)
                if deleteLabConfirmation == "true":
                    deleteLabConfirmation = True
                if deleteLabConfirmation:
                    removed = setLabInactive(labID=currentLID)
                    removed = removed and removeLabFromAccount(labID=currentLID, userID=request.user)
                    if removed:
                    #Removed successfully
                        return redirect('/app')
                    else:
                        return render(
                            request,
                            'app/error.html',
                            {
                                'title': "Error",
                                'message': "The lab was not deleted. Please contact us",
                                'year': datetime.now(utc).year
                            }
                        )
                return redirect('/lab/manageLab')
            elif 'addTAForm' in request.POST:  # If a TA is added to the lab
                if addTAform.is_valid():
                    addTAform.save()
                    return redirect('/lab/manageLab')
                else:
                    pass
            else:  # Either create or delete lab code
                labCodeToRemove = request.POST.get("labCodeToRemove", "")
                createLabCodeRole = request.POST.get("role", "")
                if labCodeToRemove != "":  # Remove lab code
                    deleteLabCode(labCodeToRemove)
                else:  # Create lab code
                    generateLabCode(labID=currentLID, role=createLabCodeRole)
                return redirect('/lab/manageLab')
        else:
            form = ManageLabForm(prefix='detailsForm',
                                 lid=currentLID, initial=initialData)
            notificationForm = ManageLabNotificationsForm(prefix='notificationForm',
                                                          user=request.user,
                                                          lid=currentLID,
                                                          initial=initialData)
            studentLabCode = getLabCode(currentLID, 's')
            taLabCode = getLabCode(currentLID, 't')
            students = getLabUsersWithRole(labID=currentLID, role='s')
            tas = getLabUsersWithRole(labID=currentLID, role='t')
            addTAform = AddTAForm(prefix='addTAForm', lid=currentLID)
        return render(
            request,
            'app/manageLab.html',
            {
                'title': 'Manage Lab',
                'message': 'Edit lab settings',
                'year': datetime.now().year,
                'detailsForm': form,
                'notificationForm': notificationForm,
                'studentLabCode': studentLabCode,
                'taLabCode': taLabCode,
                'students': students,
                'tas': tas,
                'addTAform': addTAform
            }
        )
    #If the user if a TA for the current lab
    elif (getRole(userID=request.user, labID=currentLID) == 't'):
        userNotificationSettings = getNotificationSettings(userID=request.user, labID=currentLID)
        if userNotificationSettings == None:
            userNotificationSettings = Notify(uid_id=request.user.id,
                                              lid_id=currentLID,
                                              notifyNew=False,
                                              notifyThreshold=0)
            userNotificationSettings.save()
        initialData["notifyNew"] = userNotificationSettings.notifyNew
        initialData["notifyThreshold"] = userNotificationSettings.notifyThreshold
        if request.method == 'POST':
            notificationForm = ManageLabNotificationsForm(request.POST, user=request.user, lid = currentLID)
            if notificationForm.is_valid():
                notificationForm.save()
                return redirect('/lab/manageLab')
        else:
            notificationForm = ManageLabNotificationsForm(user = request.user, lid = currentLID, initial=initialData)
            return render(
                request,
                'app/manageLabTA.html',
                {
                    'title': 'Manage Lab',
                    'message': 'Edit Lab Settings',
                    'year': datetime.now().year,
                    'notificationForm': notificationForm,
                }
            )
    else:
        # User is not the professor for the current lab (Do not load the page)
        return render(
            request,
            'app/permissionDenied.html',
            {
                'title': 'Permission Denied',
                'message': 'You do not have permission to view this page',
                'year': datetime.now().year
            }
        )

def labFeedback(request):
    """Renders feedback page for professors"""
    # Should only render if user's role is professor
    assert isinstance(request, HttpRequest)
    currentLID = request.session.get('currentLab')
    role = getRole(userID=request.user, labID = currentLID)
    avgWait = getAvgWait(currentLID)
    avgFeedback = getAvgFeedback(currentLID)
    numRequestsComplete = getNumComplete(currentLID)
    numOutstandingRequests = getRequestCount(currentLID)
    if(role == 'p'):
        #User is a prof and should have access
        return render(
            request,
            'app/labFeedback.html',
            {
                'title': 'Feedback',
                'message': 'View feedback, wait time, and other lab metrics',
                'year': datetime.now().year,
                'role': role,
                'avgWait': avgWait,
                'avgFeedback': avgFeedback,
                'numRequestsComplete': numRequestsComplete,
                'numOutstandingRequests': numOutstandingRequests
            }
        )
    else:
        #User is not a professor, render access denied
        return render(
            request,
            'app/permissionDenied.html',
            {
                'title': 'Permission Denied',
                'message': 'You do not have permission to view this page',
                'year': datetime.now().year
            }
        )

def labFeedbackHelper(request):
    """Renders feedback page for specific TA for specific lab"""
    # Should only render if user's role is professor or the specified TA
    assert isinstance(request, HttpRequest)
    pass

def manageAccountSetTab(tab):
    """Function to set the active tab for the manageAccount page"""
    retDict = {
        'accountDetails': "",
        'changePassword': ""
        }
    retDict[tab] = "in active"
    return retDict
def manageAccount(request):
    """Renders page to edit account settings"""
    assert isinstance(request, HttpRequest)
    initialAccountDetails = {
        'firstname': request.user.first_name,
        'lastname': request.user.last_name,
        'email': request.user.email
    }
    changePasswordForm = ChangePasswordForm(user=request.user)
    editAccountDetailsForm = EditAccountDetailsForm(
        user=request.user, initial=initialAccountDetails)
    activeDict = manageAccountSetTab("accountDetails") # Default tab is accountDetails
    if request.method == 'POST':
        if 'changePassword' in request.POST:
            changePasswordForm = ChangePasswordForm(data=request.POST, user=request.user)
            activeDict = manageAccountSetTab("changePassword")
            if changePasswordForm.is_valid():
                changePasswordForm.save()
                update_session_auth_hash(request, changePasswordForm.user)  #Update the session to keep the user logged in
            #return redirect('/account')
        elif 'editAccountDetails' in request.POST:
            form = EditAccountDetailsForm(
                data=request.POST, user=request.user, initial=initialAccountDetails)
            if form.is_valid():
                form.save()
            return redirect('/account')
        elif 'deleteAccount' in request.POST:
            deleteResponse = request.POST.get('deleteAccount', False)
            if deleteResponse == "true":
                delete = deleteAccount(request.user.id)
                if delete == True:
                    return redirect('/')  # Account deleted
                else:
                    return render(
                        request,
                        'app/error.html',
                        {
                            'title': "Error",
                            'message': str(delete[1]),
                            'year':datetime.now().year
                        }
                    )
            else:
                return redirect('/account') # Unknown error. Should never reach
        else:
            print("Error")
            return redirect('/account')
    return render(
        request,
        'app/account.html',
        {
            'title': 'Manage Account',
            'message': 'Manage Account',
            'year': datetime.now().year,
            'changePasswordForm': changePasswordForm,
            'editAccountDetailsForm': editAccountDetailsForm,
            'active': activeDict
        }
    )

def currentRequest(request):
    """Renders page to edit account settings"""
    assert isinstance(request, HttpRequest)
    currentLID = request.session.get('currentLab')
    role = getRole(userID=request.user, labID=currentLID)
    if (role == 'p' or role == 't'):
        #User is a prof or TA and should have access
        openRequest = getOutstandingRequest(labID=currentLID, userID=request.user)
        nextRequest = None
        if openRequest != None:
            nextRequest = openRequest
        else:
            nextRequest = getNextRequest(currentLID)
        nextRequest.huid = request.user
        nextRequest.save()
        return render(
            request,
            'app/currentRequest.html',
            {
                'title': 'Current Request',
                'nameOfUser': getNameOfUser(nextRequest.suid_id),
                'station': nextRequest.station,
                'description': nextRequest.description,
                'requestSubmitted': str(nextRequest.timeSubmitted),
                'averageWait' : getAvgWait(currentLID),
                'requests' : str(getRequestCount(currentLID)),
                'year': datetime.now(utc).year
            }
        )
    else:
        #User is a student, render access denied
        return render(
            request,
            'app/permissionDenied.html',
            {
                'title': 'Permission Denied',
                'message': 'You do not have permission to view this page',
                'year': datetime.now().year
            }
        )

def professor(request):
    """Renders page to allow professors to navigate"""
    assert isinstance(request, HttpRequest)
    pass

def ta(request):
    """Renders page to allow TA's to navigate"""
    assert isinstance(request, HttpRequest)
    pass

def forgotPassword(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    if (request.method == "POST"):
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            user = getUserByEmail(form.save())
            if (user != None):
                prc = generatePasswordResetCode(user.id)
                sendPasswordReset(user, prc.prc)
                return redirect('/')
            else:
                #No user found with that email
                return render(
                    request,
                    'app/error.html',
                    {
                        'title': "Error",
                        'message': "No account with that email was found",
                        'year': datetime.now().year,
                    }
                )
    else:
        form = ForgotPasswordForm()
        return render(
            request,
            'app/forgotPassword.html',
            {
                'title': 'Forgot Password',
                'message' : "If an account is found with your email, a password reset link will be sent to your email",
                'form' : form,
                'year': datetime.now().year,
            }
        )

def resetPassword(request, prc):
    """Renders the reset password page."""
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password=form.save()
            if new_password != False:
                result = resetPasswordFunc(prc, new_password)
                if result:
                    return redirect('/login')
                else:
                    return render(
                        request,
                        'app/error.html',
                        {
                            'title': "Error",
                            'message': 'The Password Reset Code was not found',
                            'year': datetime.now().year
                        }
                    )
            else:
                return render(
                    request,
                    'app/error.html',
                    {
                        'title': 'Error',
                        'message': 'The passwords do not match. Please try again',
                        'year': datetime.now().year
                    }
                )
        else:
            return redirect('/')  #TODO: Change this
    else:
        form = ResetPasswordForm()
        return render(
            request,
            'app/resetPassword.html',
            {
                'title': 'Reset Password',
                'message': 'Set a new password for your LabLineup account',
                'year': datetime.now().year,
                'form': form,
            }
        )

def confirmAccountView(request, regConCode):
    assert isinstance(request, HttpRequest)
    if confirmAccount(regConCode=regConCode):
        #Code is found, account is activated
        return render(
            request,
            'app/accountConfirmation.html',
            {
                'title': 'Account Confirmed',
                'message': 'Your account has been activated.',
                'year': datetime.now().year,
                'accountConfirmed': True
            }
        )
    else:
        #Code is not found
        return render(
            request,
            'app/accountConfirmation.html',
            {
                'title': 'Account Confirmation Failed',
                'message': 'The account confirmation link is invalid.',
                'year': datetime.now().year,
                'accountConfirmed': False
            }
        )

def requestEmailConfirmation(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = RequestEmailConfirmForm(request.POST)
        if form.is_valid():
            output = form.save()
            rcc = generateRegConCode(output.id)
            sendRegistrationConfirmation(output, rcc.regConCode)
            return render(
                request,
                'app/message.html',
                {
                    'title':"Welcome to LabLineup",
                    'message': "Please check your email for a link to activate your account.",
                    'year': datetime.now().year
                }
            )
        else:
            pass
    else:
        form = RequestEmailConfirmForm()
    return render(
        request,
        'app/requestEmailConfirm.html',
        {
            'title': 'Confirm Registration',
            'message:': 'Please enter your username below to send a new registration confirmation email',
            'year': datetime.now().year,
            'form': form
        }
    )

def requestHistory(request):
    assert(isinstance(request, HttpRequest))
    requestsDict = getRequestHistory(userID=request.user)
    return render(
        request,
        'app/requestHistory.html',
        {
            'title': "Request History",
            'message': "View request history",
            'year': datetime.now().year,
            'requests': requestsDict
        }
    )
