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
from app.forms import ContactForm

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
from app.modelFunc import getUnassignedRequestCount
from app.modelFunc import getUserByEmail
from app.modelFunc import generatePasswordResetCode
from app.modelFunc import resetPasswordFunc
from app.modelFunc import getNotificationSettings
from app.modelFunc import generateRegConCode
from app.modelFunc import confirmAccount
from app.modelFunc import getAvgWait
from app.modelFunc import getNextRequest
from app.modelFunc import getNameOfUser
from app.modelFunc import getStudentCurrentRequest
from app.modelFunc import getOutstandingRequest
from app.modelFunc import removeLabFromAccount
from app.modelFunc import getLabUsersWithRole
from app.modelFunc import setLabInactive
from app.modelFunc import deleteAccount
from app.modelFunc import getRequestHistory
from app.modelFunc import getNumComplete
from app.modelFunc import getAvgFeedback
from app.modelFunc import getLastRequest
from app.modelFunc import updateSub
from app.modelFunc import updateSubOrder
from app.modelFunc import confirmNewSub
from app.modelFunc import getSub
from app.modelFunc import cancelRequest
from app.modelFunc import convertToLocal
from app.modelFunc import getAvgWaitTA
from app.modelFunc import getAvgFeedbackTA
from app.modelFunc import getNumCompleteTA
from app.modelFunc import getNumOutstandingRequestsTA
from app.modelFunc import updateFeedback
from app.modelFunc import markRequestComplete
from app.modelFunc import getRequests
from app.modelFunc import assignRequest
from app.modelFunc import releaseRequest
from app.modelFunc import markRequestNotComplete
from app.modelFunc import getFeedbackCount
from app.modelFunc import taViewFeedback
from app.modelFunc import getLabsWithRoleStudent
from app.modelFunc import getLabsWithRoleHelper
from app.modelFunc import userExists
from app.modelFunc import getLabName

from app.SendEmail import sendAllRequest
from app.SendEmail import sendPasswordReset
from app.SendEmail import sendRegistrationConfirmation
from app.SendEmail import sendNeverHelped
from app.SendEmail import sendTransferredRequest
from app.SendEmail import sendContactForm

from app.Payment import createCheckout
from app.Payment import findRecentPayment
from app.Payment import findProductOrder

from app.Alert import getAlerts


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
        seen = request.POST.get("home")
        if int(seen) == 1:
            request.session["splashSeen"] = True
    splashSeen = request.session.get("splashSeen")
    if splashSeen:
        return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
            'alerts': getAlerts(request.user.id)
        }
    )
    else:
        return render(
            request,
            'app/splashScreen.html',
            {
                'title': 'Home Page',
                'year': datetime.now().year,
                'alerts': getAlerts(request.user.id)
            }
        )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            human = True
            output = form.save()
            firstName = request.POST.get('firstName', '')
            lastName = request.POST.get('lastName', '')
            email = request.POST.get('email', '')
            phoneNumber = request.POST.get('phoneNumber', '')
            message = request.POST.get('message', '')

            #CALL fxn to submit msg to LL email
            sendContactForm(firstName, lastName, email, phoneNumber, message)
            return redirect('/contact/confirm')
    else:
        form = ContactForm()
    return render(
        request,
        'app/contact.html',
        {
            'title': 'Contact Us',
            'message': 'Please feel free to contact us with any suggestions or comments.',
            'year': datetime.now().year,
            'form': form,
            'alerts': getAlerts(request.user.id)
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
            'alerts': getAlerts(request.user.id)
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
                        'year': datetime.now().year,
                        'alerts': getAlerts(request.user.id)
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
            'form': form,
            'alerts': getAlerts(request.user.id)
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
            'alerts': getAlerts(request.user.id)
        }
    )

def createLab(request):
    """Renders the createLab page. """
    assert isinstance(request, HttpRequest)
    if not request.user.is_authenticated:
        return render(request,
                      'app/notLoggedIn.html',{'year':datetime.now(utc).year})
    labLimit = getLabLimit(userID=request.user)
    if (labLimit != None and getNumberOfLabs(userID=request.user) >= labLimit):
        return render(
            request,
            'app/error.html',
            {
                'title': "Error",
                'message': "You have reached your limit for labs as a professor. Please upgrade your subscription.",
                'year': datetime.now().year,
                'alerts': getAlerts(request.user.id)
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
                'form': form,
                'alerts': getAlerts(request.user.id)
            }
        )

def addLab(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    if not request.user.is_authenticated:
        return render(request,
                      'app/notLoggedIn.html',{'year':datetime.now(utc).year})
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
            'alerts': getAlerts(request.user.id)
        }
    )

def selectLab(request):
    """Renders main app page (select a lab)"""
    assert isinstance(request, HttpRequest)
    if not request.user.is_authenticated:
        return render(request,
                      'app/notLoggedIn.html',{'year':datetime.now(utc).year})
    if request.method == 'POST':
        selectedLabID = request.POST.get("labID", None)
        selectedLabIDRemove = request.POST.get("labIDRemove", None)
        if selectedLabID != None:
            request.session["currentLab"] = selectedLabID
            role = getRole(userID=request.user, labID=selectedLabID)
            if role == 's':
                currReq = getStudentCurrentRequest(labID=selectedLabID, userID=request.user)
                if currReq != None:
                    #If the student has an open request
                    request.session["currentRequest"] = currReq.rid
                    return redirect('/student/requestSubmitted')
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
                        'year': datetime.now(utc).year,
                        'alerts': getAlerts(request.user.id)
                    }
                )
    else:
        # Lists of dictionaries of lab objects and count of open request(s)
        labsWhereStudent = getLabsWithRoleStudent(userID=request.user)
        labsWhereTA = getLabsWithRoleHelper(userID=request.user, role='t')
        labsWhereProfessor = getLabsWithRoleHelper(userID=request.user, role='p')
        return render(
            request,
            'app/selectLab.html',
            {
                'title': 'Select Lab',
                'message': 'Select a lab',
                'year': datetime.now(utc).year,
                'labsWhereStudent': labsWhereStudent,
                'labsWhereTA': labsWhereTA,
                'labsWhereProfessor': labsWhereProfessor,
                'alerts': getAlerts(request.user.id)
            }
        )

def studentRequest(request):
    """Renders page for student to submit request."""
    # Should only render if user's role is student
    # Blank Request Form => Request Waiting Form => Feedback Form
    assert isinstance(request, HttpRequest)
    if not request.user.is_authenticated:
        return render(request,
                      'app/notLoggedIn.html',{'year':datetime.now(utc).year})
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
                'title': 'Submit Request for ',
                'message': 'Submit a request for help',
                'year': datetime.now().year,
                'form': form,
                'alerts': getAlerts(request.user.id),
                "lab":getLabName(currentLID)
            }
        )
    else:
        return render(
            request,
            'app/permissionDenied.html',
            {
                'title': 'Permission Denied',
                'message': 'You do not have permission to view this page',
                'year': datetime.now().year,
                'alerts': getAlerts(request.user.id)
            }
        )

def studentRequestSubmitted(request):
    """Renders pages for lab/{labID}/student."""
    # Blank Request Form => Request Waiting Form => Feedback Form
    assert isinstance(request, HttpRequest)
    if not request.user.is_authenticated:
        return render(request,
                      'app/notLoggedIn.html',{'year':datetime.now(utc).year})
    currentLID = request.session.get('currentLab')
    avgWait = getAvgWait(currentLID)
    numBefore = 0
    lab = Lab.objects.get(lid=currentLID)
    try:
        currRequest = Request.objects.get(lid=currentLID, suid=request.user, timeCompleted=None)
    except:
        currRequest = None
    if currRequest == None:
        return redirect('/student/requestFeedback')
    allRequests = getRequests(currentLID)
    for req in allRequests:
        if (req.suid != request.user):
            numBefore += 1
        else:
            break
    # Should only render if user's role is student
    if (getRole(userID=request.user, labID=currentLID) == 's'):
        if request.method == 'POST':
            # If lab is not active, student should get redirect
            if lab.active == False:
                return render(
                    request,
                    'app/permissionDenied.html',
                    {
                        'title': 'Permission Denied',
                        'message': 'We\'re sorry. This lab is no longer active. Please contact your professor',
                        'year': datetime.now().year,
                        'alerts': getAlerts(request.user.id)
                    }
                )
            if 'neverHelped' in request.POST:
                sendNeverHelped(currentLID, request.user, currRequest.rid)
                markRequestNotComplete(rid=currRequest.rid)
                return redirect('/app')
            if 'cancelRequest' in request.POST:
                cancelled = cancelRequest(currRequest)
                if cancelled:
                    return redirect('/app')
                else:
                    return render(
                        request,
                        'app/error.html',
                        {
                            'title': "Error",
                            'message': "Request was not deleted.",
                            'year': datetime.now(utc).year,
                            'alerts': getAlerts(request.user.id)
                           }
                    )
            return redirect('/student/requestSubmitted')
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
                'numBefore': numBefore,
                'description': currRequest.description,
                'alerts': getAlerts(request.user.id)
            }
        )
    else:
        return render(
            request,
            'app/permissionDenied.html',
            {
                'title': 'Permission Denied',
                'message': 'You do not have permission to view this page',
                'year': datetime.now().year,
                'alerts': getAlerts(request.user.id)
            }
        )

def studentRequestFeedback(request):
    """Renders pages for lab/{labID}/student."""
    # Blank Request Form => Request Waiting Form => Feedback Form
    assert isinstance(request, HttpRequest)
    if not request.user.is_authenticated:
        return render(request,
                      'app/notLoggedIn.html',{'year':datetime.now(utc).year})
    currentLID = request.session.get('currentLab')
    currentRequest = request.session.get('currentRequest')
    message = 'Please submit feedback about the help you received'
    # Should only render if user's role is student
    if (getRole(userID=request.user, labID=currentLID) == 's'):
        if request.method == 'POST':
            if 'score' in request.POST:
                score = int(request.POST.get('score', 0))
                if(score == 0):
                    message = 'You forgot to select a score'
                    pass
                else:
                    updateFeedback(currentRequest, score)
                    return redirect('/student/request')
            else:
                pass
        return render(
            request,
                'app/studentRequestFeedback.html',
                {
                    'title': 'Feedback',
                    'message': message,
                    'year': datetime.now().year,
                    'alerts': getAlerts(request.user.id)
                }
        )
    else:
        return render(
            request,
                'app/permissionDenied.html',
                {
                    'title': 'Permission Denied',
                    'message': 'You do not have permission to view this page',
                    'year': datetime.now().year,
                    'alerts': getAlerts(request.user.id)
                }
            )

def labQueue(request):
    """Renders queue for lab (for TA's and professors)"""
    # Should only render if user's role is TA or professor
    assert isinstance(request, HttpRequest)
    if not request.user.is_authenticated:
        return render(request,
                      'app/notLoggedIn.html',{'year':datetime.now(utc).year})
    currentLID = request.session.get('currentLab')
    lab = Lab.objects.get(lid=currentLID)
    role = getRole(userID=request.user, labID = currentLID)
    if (role == 'p' or role == 't'):
        openRequest = getOutstandingRequest(labID=currentLID, userID=request.user.id)
        if openRequest != None:
            return redirect("/lab/queue/currentRequest")
        return render(
            request,
            'app/queue.html',
            {
                'title' : lab.name,
                'message': 'Queue',
                'year': datetime.now().year,
                'role': role,
                'requestCount': str(getUnassignedRequestCount(currentLID)),
                'averageWait': str(getAvgWait(currentLID)),
                'alerts': getAlerts(request.user.id)
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
                'year': datetime.now().year,
                'alerts': getAlerts(request.user.id)
            }
        )

def labManage(request):
    """Renders manage lab page for professors and TAs (pages will be different)"""
    # Should only render if user's role is professor
    assert isinstance(request, HttpRequest)
    if not request.user.is_authenticated:
        return render(request,
                      'app/notLoggedIn.html',{'year':datetime.now(utc).year})
    currentLID = request.session.get('currentLab')
    currentLab = Lab.objects.get(lid=currentLID)
    initialData = {
        'lid': currentLID,
        'labName': currentLab.name,
        'labDescription': currentLab.description,
        'taViewFeedback': currentLab.taViewFeedback,
        'open': currentLab.open
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
        form = ManageLabForm(prefix='detailsForm',
                                     lid=currentLID,
                                     initial=initialData)
        notificationForm = ManageLabNotificationsForm(user=request.user,
                                                          prefix='notificationForm',
                                                          lid=currentLID,
                                                          initial=initialData)
        studentLabCode = getLabCode(currentLID, 's')
        taLabCode = getLabCode(currentLID, 't')
        students = getLabUsersWithRole(labID=currentLID, role='s')
        tas = getLabUsersWithRole(labID=currentLID, role='t')
        addTAform = AddTAForm(prefix='addTAForm', lid=currentLID)
        if request.method == 'POST':
            if 'detailsForm' in request.POST:  # If the lab name/description was saved
                form = ManageLabForm(request.POST,
                                     prefix='detailsForm',
                                     lid=currentLID,
                                     initial=initialData)
                if form.is_valid():
                    form.save()
                    return redirect('/lab/manageLab')
            elif 'notificationForm' in request.POST:  # If the notification settings were updated
                notificationForm = ManageLabNotificationsForm(request.POST,
                                                              user=request.user,
                                                              prefix='notificationForm',
                                                              lid=currentLID)
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
                            'year': datetime.now(utc).year,
                            'alerts': getAlerts(request.user.id)
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
                                'year': datetime.now(utc).year,
                                'alerts': getAlerts(request.user.id)
                            }
                        )
                return redirect('/lab/manageLab')
            elif 'addTAForm' in request.POST:  # If a TA is added to the lab
                addTAform = AddTAForm(request.POST, prefix='addTAForm', lid=currentLID)
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
                'addTAform': addTAform,
                'alerts': getAlerts(request.user.id)
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
                'alerts': getAlerts(request.user.id)
            }
        )
    else:
        # User is not the professor or TA for the current lab (Do not load the page)
        return render(
            request,
            'app/permissionDenied.html',
            {
                'title': 'Permission Denied',
                'message': 'You do not have permission to view this page',
                'year': datetime.now().year,
                'alerts': getAlerts(request.user.id)
            }
        )

def labFeedback(request):
    """Renders feedback page for professors"""
    # Should only render if user's role is professor
    assert isinstance(request, HttpRequest)
    if not request.user.is_authenticated:
        return render(request,
                      'app/notLoggedIn.html',{'year':datetime.now(utc).year})
    currentLID = request.session.get('currentLab')
    role = getRole(userID=request.user, labID = currentLID)
    if(role == 'p'):
        #User is a prof and should have access
        avgWait = getAvgWait(currentLID)
        avgFeedback = getAvgFeedback(currentLID)
        numRequestsComplete = getNumComplete(currentLID)
        numOutstandingRequests = getRequestCount(currentLID)
        helpers = [request.user]
        labTAs = getLabUsersWithRole(labID=currentLID, role='t')
        for ta in labTAs:
            helpers.append(ta)
        if request.method == 'POST':
            currentHID = request.session.get("currentHelper")
            if 'newHelperID' in request.POST:
                newHelperID = int(request.POST.get("newHelperID", 0))
                if newHelperID != 0:
                    return redirect("helper/" + str(newHelperID) + "/")
                else:
                    pass
            else:
                return render(request,
                              'app/error.html',
                              {
                                  'title': "Error!",
                                  'message': "An unknown error has occurred",
                                  'alerts': getAlerts(request.user.id)
                              }
                             )
        return render(
            request,
            'app/labFeedback.html',
            {
                'title': 'Feedback',
                'message': 'View feedback, wait time, and other lab metrics',
                'year': datetime.now().year,
                'role': role,
                'avgWait': avgWait,
                'avgFeedback': round(avgFeedback,1),
                'numRequestsComplete': numRequestsComplete,
                'numOutstandingRequests': numOutstandingRequests,
                'labTAs': helpers,
                'alerts': getAlerts(request.user.id)
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
                'year': datetime.now().year,
                'alerts': getAlerts(request.user.id)
            }
        )

def labFeedbackHelper(request, userID):
    """Renders feedback page for specific TA for specific lab"""
    # Should only render if user's role is professor or the specified TA
    assert isinstance(request, HttpRequest)
    if not request.user.is_authenticated:
        return render(request,
                      'app/notLoggedIn.html',{'year':datetime.now(utc).year})
    currentLID = request.session.get('currentLab')
    role = getRole(userID=request.user, labID = currentLID)
    nameOfTA = getNameOfUser(userID=userID)
    avgWaitTA = getAvgWaitTA(currentLID, userID)
    avgFeedbackTA = getAvgFeedbackTA(currentLID, userID)
    numRequestsCompleteTA = getNumCompleteTA(currentLID, userID)
    numOutstandingRequestsTA = getNumOutstandingRequestsTA(currentLID, userID)
    feedbackCount = getFeedbackCount(currentLID, userID=userID)
    taViewAllowed = taViewFeedback(currentLID) and role == 't' and request.user.id == userID
    if (role == 'p' or taViewAllowed) and feedbackCount >= 3:
        #User is a prof, feedback should display immediately
        #Or User is a TA with permission, feedback should render
        return render(
            request,
            'app/labFeedbackTA.html',
            {
                'title': 'TA Feedback',
                'nameOfTA': nameOfTA,
                'message': 'View feedback, wait time, and other lab metrics for this TA',
                'year': datetime.now().year,
                'role': role,
                'avgWaitTA': avgWaitTA,
                'avgFeedbackTA': round(avgFeedbackTA,1),
                'numRequestsCompleteTA': numRequestsCompleteTA,
                'numOutstandingRequestsTA': numOutstandingRequestsTA,
                'alerts': getAlerts(request.user.id)
             }
        )
    elif (role == 'p' or taViewAllowed) and feedbackCount < 3:
        # User is a prof or TA with permission,
        # but does not have enough ratings to review feedback
        return render(
            request,
            'app/error.html',
            {
                'title': "Not Enough Feedback",
                'message': "This user has not received enough feedback to be viewed.",
                'year': datetime.now(utc).year,
                'alerts': getAlerts(request.user.id)
            }
        )

    else:
        # User is not a professor or TA (or is a TA without permission),
        # render access denied
        return render(
            request,
            'app/permissionDenied.html',
            {
                'title': 'Permission Denied',
                'message': 'You do not have permission to view this page',
                'year': datetime.now().year,
                'alerts': getAlerts(request.user.id)
            }
        )

def manageAccountSetTab(tab):
    """Function to set the active tab for the manageAccount page"""
    retDict = {
        'accountDetails': "",
        'changePassword': "",
        'subscription': ""
        }
    retDict[tab] = "in active"
    return retDict
def manageAccount(request):
    """Renders page to edit account settings"""
    assert isinstance(request, HttpRequest)
    if not request.user.is_authenticated:
        return render(request,
                      'app/notLoggedIn.html',{'year':datetime.now(utc).year})
    initialAccountDetails = {
        'firstname': request.user.first_name,
        'lastname': request.user.last_name,
        'email': request.user.email
    }
    changePasswordForm = ChangePasswordForm(user=request.user)
    editAccountDetailsForm = EditAccountDetailsForm(
        user=request.user, initial=initialAccountDetails)
    userSub = getSub(request.user.id)
    if userSub == None:
            userSub = Subscription(uid_id = request.user.id,
                                   initialSub = None,
                                   lastSub = None,
                                   subRenewal = None,
                                   labLimit = 1)
            userSub.save()
    # Default tab is accountDetails
    activeDict = manageAccountSetTab("accountDetails")
    if request.method == 'POST':
        if 'changePassword' in request.POST:
            changePasswordForm = ChangePasswordForm(data=request.POST,
                                                   user=request.user)
            activeDict = manageAccountSetTab("changePassword")
            if changePasswordForm.is_valid():
                changePasswordForm.save()
                #Update the session to keep the user logged in
                update_session_auth_hash(request, changePasswordForm.user)
            #return redirect('/account')
        elif 'editAccountDetails' in request.POST:
            editAccountDetailsForm = EditAccountDetailsForm(data=request.POST,
                user=request.user,
                initial=initialAccountDetails)
            if editAccountDetailsForm.is_valid():
                editAccountDetailsForm.save()
        elif 'subPlan' in request.POST:
            activeDict = manageAccountSetTab("subscription")
            plan = int(request.POST.get("subPlan", 0))
            checkoutLink = createCheckout(request.user.id,
                                          userSub.id,
                                          plan)
            if checkoutLink != None:
                return redirect(checkoutLink)
            else:
                return render(
                        request,
                        'app/error.html',
                        {
                            'title': "Error",
                            'message': "Checkout failed. Please contact us.",
                            'year':datetime.now().year,
                            'alerts': getAlerts(request.user.id)
                        }
                    )
            #Check if payment recieved. If so, updateSub(userID, plan#)
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
                            'year':datetime.now().year,
                            'alerts': getAlerts(request.user.id)
                        }
                    )
            else:
                return redirect('/account') # Unknown error. Should never reach
        else:
            print("Error")
            return redirect('/account')
    numLabsUsed = getNumberOfLabs(request.user.id)
    currentPlan = "Free"
    temp = findProductOrder(findRecentPayment(userSub.id)[1])
    if temp != None:
        currentPlan = temp
    return render(
        request,
        'app/account.html',
        {
            'title': 'Manage Account',
            'message': 'Manage Account',
            'year': datetime.now().year,
            'changePasswordForm': changePasswordForm,
            'editAccountDetailsForm': editAccountDetailsForm,
            'active': activeDict,
            'userSub': userSub,
            'labsUsed': numLabsUsed,
            'labsPercentUsed': int(round(numLabsUsed/userSub.labLimit*100, 0)),
            'userSubPlan': currentPlan,
            'alerts': getAlerts(request.user.id)
        }
    )

def currentRequest(request):
    """Renders page to edit account settings"""
    assert isinstance(request, HttpRequest)
    if not request.user.is_authenticated:
        return render(request,
                      'app/notLoggedIn.html',{'year':datetime.now(utc).year})
    currentLID = request.session.get('currentLab')
    currentUserID = userID = request.user.id
    role = getRole(userID=request.user, labID=currentLID)
    if (role == 'p' or role == 't'):
        #User is a prof or TA and should have access
        if request.method == 'POST':
            currentRID = request.session.get("currentRID")
            if 'newHelperID' in request.POST:
                newHelperID = int(request.POST.get("newHelperID", 0))
                if newHelperID != 0:
                    assignRequest(currentRID, newHelperID)
                    sendTransferredRequest(currentLID, currentRID, currentUserID)
                return redirect("/lab/queue")
            elif 'markComplete' in request.POST:
                #Mark the request as complete
                markRequestComplete(currentRID)
                return redirect('/lab/queue')
            elif 'releaseRequest' in request.POST:
                #Releasing the request (user is not helping right now)
                releaseRequest(currentRID)
                return redirect("/lab/queue")
            else:
                #This should never be reached
                return render(request,
                              'app/error.html',
                              {
                                  'title' : "Error",
                                  'message': "An error occured",
                                  'year': datetime.now(utc).year,
                                  'alerts': getAlerts(request.user.id)
                              }
                              )
        else:
            #If not post, then assign a new request
            openRequest = getOutstandingRequest(labID=currentLID, userID=currentUserID)
            nextRequest = None
            if openRequest != None:
                nextRequest = openRequest
            else:
                nextRequest = getNextRequest(currentLID)
            if nextRequest != None:
                #If the lab has a request to show
                assignRequest(nextRequest.rid, currentUserID)
                request.session["currentRID"] = nextRequest.rid
                requestSubmitted = str(nextRequest.timeSubmitted.date())
                requestSubmitted = requestSubmitted + " " + str(nextRequest.timeSubmitted.strftime("%X"))
                labProfs = getLabUsersWithRole(labID=currentLID, role='p')
                labTAs = getLabUsersWithRole(labID=currentLID, role='t')
                #Remove current user from transfer list
                if role == 'p':
                    for user in labProfs:
                        if user.id == currentUserID:
                            #If the user is the professor
                            labProfs.remove(user)
                else:
                    for user in labTAs:
                        if user.id == currentUserID:
                            #If the user is a TA
                            labTAs.remove(user)
                return render(
                    request,
                    'app/currentRequest.html',
                    {
                        'title': 'Current Request',
                        'nameOfUser': getNameOfUser(nextRequest.suid_id),
                        'station': nextRequest.station,
                        'description': nextRequest.description,
                        'requestSubmitted': requestSubmitted,
                        'averageWait' : getAvgWait(currentLID),
                        'requests' : str(getRequestCount(currentLID)),
                        'labProfs': labProfs,
                        'labTAs': labTAs,
                        'year': datetime.now(utc).year,
                        'alerts': getAlerts(request.user.id)
                    }
                )
            else:
                return redirect("/lab/queue")
    else:
        #User is a student, render access denied
        return render(
            request,
            'app/permissionDenied.html',
            {
                'title': 'Permission Denied',
                'message': 'You do not have permission to view this page',
                'year': datetime.now(utc).year,
                'alerts': getAlerts(request.user.id)
            }
        )

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
                        'alerts': getAlerts(request.user.id)
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
                'alerts': getAlerts(request.user.id)
            }
        )

def resetPassword(request, prc):
    """Renders the reset password page."""
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password=form.save()
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
                        'year': datetime.now().year,
                        'alerts': getAlerts(request.user.id)
                    }
                )
        else:
            pass #Return with errors
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
            'alerts': getAlerts(request.user.id)
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
                'accountConfirmed': True,
                'alerts': getAlerts(request.user.id)
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
                'accountConfirmed': False,
                'alerts': getAlerts(request.user.id)
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
                    'year': datetime.now().year,
                    'alerts': getAlerts(request.user.id)
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
            'form': form,
            'alerts': getAlerts(request.user.id)
        }
    )

def requestHistory(request):
    assert(isinstance(request, HttpRequest))
    if not request.user.is_authenticated:
        return render(request,
                      'app/notLoggedIn.html',{'year':datetime.now(utc).year})
    requestsDict = getRequestHistory(mode="Student", studentID=request.user)
    return render(
        request,
        'app/requestHistory.html',
        {
            'title': "Request History",
            'message': "View request history",
            'year': datetime.now().year,
            'requests': requestsDict,
            'alerts': getAlerts(request.user.id)
        }
    )

def requestHistoryProf(request):
    assert(isinstance(request, HttpRequest))
    if not request.user.is_authenticated:
        return render(request,
                      'app/notLoggedIn.html',{'year':datetime.now(utc).year})
    currentLID = request.session.get('currentLab')
    if (getRole(userID=request.user, labID=currentLID) == 'p'):
        requestsDict = getRequestHistory(mode="Professor", labID=currentLID)
        return render(
            request,
            'app/requestHistoryProf.html',
            {
                'title': "Request History for " + getLabName(currentLID),
                'message': "View request history",
                'year': datetime.now().year,
                'requests': requestsDict,
                'view': "Professor",
                'alerts': getAlerts(request.user.id)
            }
        )
    else:
        # User is not the professor or TA for the current lab (Do not load the page)
        return render(
            request,
            'app/permissionDenied.html',
            {
                'title': 'Permission Denied',
                'message': 'You do not have permission to view this page',
                'year': datetime.now().year,
                'alerts': getAlerts(request.user.id)
            }
        )

def pricing(request):
    assert(isinstance(request, HttpRequest))
    return render(
        request,
        'app/pricing.html',
        {
            'title': "Pricing",
            'message': "Subscription Options",
            'year': datetime.now().year,
            'alerts': getAlerts(request.user.id)
        }
    )

def subThankYou(request):
    assert(isinstance(request, HttpRequest))
    products = {"LabLineup Silver": 1, "LabLineup Gold": 2, None:None}
    subID = int(request.GET.get("referenceId"))
    orderID = request.GET.get("transactionId")
    valid = confirmNewSub(subID, orderID)
    if valid:
        product = products[findProductOrder(orderID)]
        if product != None:
            updateSub(subID, product)
            updateSubOrder(subID, orderID)
            return render(
                request,
                'app/subTY.html',
                {
                    'title': "Thank You!",
                    'message': "Thank you for joining LabLineup Premium",
                    'year': datetime.now().year,
                    'alerts': getAlerts(request.user.id)
                }
            )
        else:
            pass
    return render(
        request,
        'app/error.html',
        {
            'title': "Error",
            'message': "Your subscription could not be updated. Please contact us.",
            'year': datetime.now().year,
            'alerts': getAlerts(request.user.id)
        }
    )

def contactConfirm(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contactConfirm.html',
        {
            'title': 'Thank You!',
            'message': "We will reply to your inquiry shortly.",
            'year': datetime.now().year,
            'alerts': getAlerts(request.user.id)
        }
    )
