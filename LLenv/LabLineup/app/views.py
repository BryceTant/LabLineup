"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from app.forms import BootstrapRegisterForm
from app.forms import AddLabForm

from app.models import Lab
from app.models import Role
from app.models import Request
from app.models import LabCode

from app.modelFunc import generateLabCode
from app.modelFunc import getLabsWithRole

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
        form = CreateLabForm(request.POST, user=request.user)
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
            #'form':form,
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

def labStudent(request, labID):
	"""Renders pages for lab/{labID}/student."""
	#Should only render if user's role is student
	#Blank Request Form => Request Waiting Form => Feedback Form
	assert isinstance(request, HttpRequest)
	pass

def labQueue(request, labID):
	"""Renders queue for lab (for TA's and professors)"""
	#Should only render if user's role is TA or professor
	assert isinstance(request, HttpRequest)
	pass

def labManage(request, labID):
	"""Renders manage lab page for professors"""
	#Should only render if user's role is professor
	assert isinstance(request, HttpRequest)
	pass

def labFeedback(request, labID):
	"""Renders feedback page for professors"""
	#Should only render if user's role is professor
	assert isinstance(request, HttpRequest)
	pass

def labFeedbackHelper(request, labID, helperID):
	"""Renders feedback page for specific TA for specific lab"""
	#Should only render if user's role is professor or the specified TA
	assert isinstance(request, HttpRequest)
	pass
