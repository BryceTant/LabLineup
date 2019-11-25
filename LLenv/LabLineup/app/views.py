"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.views.generic import CreateView

from app.forms import BootstrapRegisterForm
from app.forms import AddLabForm
from app.forms import CreateLabForm
from app.forms import ManageLabForm
from app.forms import SubmitRequestForm

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

from app.SendEmail import sendAll

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )
def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact Us',
            'message':'Please feel free to contact us with any suggestions or comments.',
            'year':datetime.now().year,
        }
    )
def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
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
			'title':'Register',
			'message:':'Create an account.',
			'year':datetime.now().year,
			'form':form
		}
	)
def help(request):
	"""Renders the about page."""
	assert isinstance(request, HttpRequest)
	return render(
        request,
        'app/help.html',
        {
            'title':'FAQs',
            'message':'Help / Frequently Asked Questions',
            'year':datetime.now().year,
        }
    )
def createLab(request):
    """Renders the createLab page. """
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = CreateLabForm(request.POST, user=request)
        if form.is_valid():
            form.save()
            return redirect('/app')
    else:
        form = CreateLabForm(user=request.user)
    return render(
        request,
        'app/createLab.html',
        {
            'title': 'Create Lab',
            'message': 'Create a lab for your class',
            'year':datetime.now().year,
            'form':form
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
            'title':'Add Lab',
            'message':'Add a lab to your account',
            'year':datetime.now().year,
			'form':form,
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
		else: #TA or professor
			return redirect('/lab/queue')
	else:
		#Lists of lab objects for each role
		labsWhereStudent = getLabsWithRole(userID=request.user, role = 's')
		labsWhereTA = getLabsWithRole(userID=request.user, role = 't')
		labsWhereProfessor = getLabsWithRole(userID=request.user, role = 'p')
		return render (
			request,
			'app/selectLab.html',
			{
				'title':'Select Lab',
				'message':'Select a lab',
				'year':datetime.now().year,
				'labsWhereStudent':labsWhereStudent,
				'labsWhereTA':labsWhereTA,
				'labsWhereProfessor':labsWhereProfessor
			}
		)
def studentRequest(request):
	"""Renders page for student to submit request."""
	#Should only render if user's role is student
	#Blank Request Form => Request Waiting Form => Feedback Form
	assert isinstance(request, HttpRequest)
	currentLID = request.session.get('currentLab')
	if (getRole(userID=request.user, labID=currentLID)=='s'):
		if request.method == 'POST':
			form = SubmitRequestForm(request.POST, user=request.user, lid=currentLID)
			if form.is_valid():
				newRID = form.save()
				request.session["currentRequest"] = newRID
				#sendAll(currentLID, getRequestCount(currentLID)) ENABLE THIS LINE FOR SENDING EMAIL NOTIFICATIONS
				return redirect('/student/requestSubmitted')
		else:
			form = SubmitRequestForm(user=request.user, lid=currentLID)
		return render(
			request,
			'app/submitRequest.html',
			{
				'title': 'Submit Request',
				'message': 'Submit a request for help',
				'year':datetime.now().year,
				'form':form
			}
		)
	else:
		return render(
			request,
			'app/permissionDenied.html',
			{
				'title':'Permission Denied',
				'message':'You do not have permission to view this page',
				'year':datetime.now().year
			}
		)
def studentRequestSubmitted(request):
	"""Renders pages for lab/{labID}/student."""
	#Should only render if user's role is student
	#Blank Request Form => Request Waiting Form => Feedback Form
	assert isinstance(request, HttpRequest)
	pass
def studentRequestFeedback(request):
	"""Renders pages for lab/{labID}/student."""
	#Should only render if user's role is student
	#Blank Request Form => Request Waiting Form => Feedback Form
	assert isinstance(request, HttpRequest)
	pass
def labQueue(request):
	"""Renders queue for lab (for TA's and professors)"""
	#Should only render if user's role is TA or professor
	assert isinstance(request, HttpRequest)
	pass
def labManage(request):
	"""Renders manage lab page for professors"""
	#Should only render if user's role is professor
	assert isinstance(request, HttpRequest)
	currentLID = request.session.get('currentLab')
	currentLab = Lab.objects.get(lid=currentLID)
	initialData = {'lid':currentLID, 
					'labName': currentLab.name,
					'labDescription':currentLab.description}
	if (getRole(userID=request.user, labID=currentLID)=='p'):  #If the user is a professor for the current lab
		#Load page to manage lab
		if request.method == 'POST':
			print (request.POST)
			if 'detailsForm' in request.POST:  #If the lab name/description was saved
				form = ManageLabForm(request.POST, prefix='detailsForm', lid=currentLID, initial=initialData)
				if form.is_valid():
					form.save()
					return redirect('/lab/queue')
			else: #Either create or delete lab code
				labCodeToRemove = request.POST.get("labCodeToRemove","")
				createLabCodeRole = request.POST.get("role","")
				if labCodeToRemove != "":  #Remove lab code
					deleteLabCode(labCodeToRemove)
				else:  #Create lab code
					generateLabCode(labID = currentLID, role=createLabCodeRole)
				return redirect('/lab/manageLab')
		else:
			form = ManageLabForm(prefix='detailsForm', lid=currentLID, initial=initialData)
			studentLabCode = getLabCode(currentLID, 's')
			taLabCode = getLabCode(currentLID, 't')
			return render(
				request,
				'app/manageLab.html',
				{
					'title':'Manage Lab',
					'message':'Edit lab settings',
					'year':datetime.now().year,
					'detailsForm':form,
					'studentLabCode':studentLabCode,
					'taLabCode':taLabCode
				}
			)
	else:
		#User is not the professor for the current lab (Do not load the page)
		return render(
			request,
			'app/permissionDenied.html',
			{
				'title':'Permission Denied',
				'message':'You do not have permission to view this page',
				'year':datetime.now().year
			}
		)
def labFeedback(request):
	"""Renders feedback page for professors"""
	#Should only render if user's role is professor
	assert isinstance(request, HttpRequest)
	pass
def labFeedbackHelper(request):
	"""Renders feedback page for specific TA for specific lab"""
	#Should only render if user's role is professor or the specified TA
	assert isinstance(request, HttpRequest)
	pass
def manageAccount(request):
	"""Renders page to edit account settings"""
	assert isinstance(request, HttpRequest)
	pass
def currentRequest(request):
	"""Renders page to edit account settings"""
	assert isinstance(request, HttpRequest)
	pass
