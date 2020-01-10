"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.views.generic import CreateView
from django.contrib.auth import update_session_auth_hash

from app.forms import BootstrapRegisterForm
from app.forms import AddLabForm
from app.forms import CreateLabForm
from app.forms import ManageLabForm
from app.forms import SubmitRequestForm
from app.forms import ChangePasswordForm
from app.forms import EditAccountDetailsForm
from app.forms import ResetPasswordForm

from app.models import Lab
from app.models import Role
from app.models import Request
from app.models import LabCode

from app.modelFunc import generateLabCode
from app.modelFunc import getLabsWithRole
from app.modelFunc import getRole
from app.modelFunc import getLabCode
from app.modelFunc import deleteLabCode
from app.modelFunc import getRequestCount
from app.modelFunc import resetPassword

from app.SendEmail import sendAllRequest


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
            'message': 'What is LabLineup?',
            'year': datetime.now().year,
        }
    )


def register(request):
    """Renders the register page."""
    assert(isinstance(request, HttpRequest))
    if request.method == 'POST':
        form = BootstrapRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
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
        selectedLabID = int(request.POST.get("labID", ""))
        request.session["currentLab"] = selectedLabID
        role = getRole(userID=request.user, labID=selectedLabID)
        if role == 's':
            return redirect('/student/request')
        else:  # TA or professor
            return redirect('/lab/queue')
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
                'year': datetime.now().year,
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
                # sendAllRequest(currentLID, getRequestCount(currentLID)) ENABLE THIS LINE FOR SENDING EMAIL NOTIFICATIONS
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
    # Should only render if user's role is student
    # Blank Request Form => Request Waiting Form => Feedback Form
    assert isinstance(request, HttpRequest)
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
    pass


def labManage(request):
    """Renders manage lab page for professors"""
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
        # Load page to manage lab
        if request.method == 'POST':
            if 'detailsForm' in request.POST:  # If the lab name/description was saved
                form = ManageLabForm(
                    request.POST, prefix='detailsForm', lid=currentLID, initial=initialData)
                if form.is_valid():
                    form.save()
                    return redirect('/lab/queue')
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
            studentLabCode = getLabCode(currentLID, 's')
            taLabCode = getLabCode(currentLID, 't')
            return render(
                request,
                'app/manageLab.html',
                {
                    'title': 'Manage Lab',
                    'message': 'Edit lab settings',
                    'year': datetime.now().year,
                    'detailsForm': form,
                    'studentLabCode': studentLabCode,
                    'taLabCode': taLabCode
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
    pass


def labFeedbackHelper(request):
    """Renders feedback page for specific TA for specific lab"""
    # Should only render if user's role is professor or the specified TA
    assert isinstance(request, HttpRequest)
    pass


def manageAccount(request):
    """Renders page to edit account settings"""
    assert isinstance(request, HttpRequest)
    initialAccountDetails = {
        'firstname': request.user.first_name,
        'lastname': request.user.last_name,
        'email': request.user.email
    }
    if request.method == 'POST':
        if 'changePassword' in request.POST:
            form = ChangePasswordForm(data=request.POST, user=request.user)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
            return redirect('/account')
        elif 'editAccountDetails' in request.POST:
            form = EditAccountDetailsForm(
                data=request.POST, user=request.user, initial=initialAccountDetails)
            if form.is_valid():
                form.save()
            return redirect('/account')
        else:
            print("Error")
            return redirect('/account')
    else:
        changePasswordForm = ChangePasswordForm(user=request.user)
        editAccountDetailsForm = EditAccountDetailsForm(
            user=request.user, initial=initialAccountDetails)
        return render(
            request,
            'app/account.html',
            {
                'title': 'Manage Account',
                'message': 'Manage Account',
                'year': datetime.now().year,
                'changePasswordForm': changePasswordForm,
                'editAccountDetailsForm': editAccountDetailsForm
            }
        )


def currentRequest(request):
    """Renders page to edit account settings"""
    assert isinstance(request, HttpRequest)
    pass


def notifications(request):
    """Renders page to edit notification settings for lab"""
    assert isinstance(request, HttpRequest)
    pass


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
    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
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
                resetPassword(request.GET.get("prc"), new_password)
                return redirect('/login')
            else:
                pass #TODO: This should show an error
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