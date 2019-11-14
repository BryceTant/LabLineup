"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from app.forms import BootstrapRegisterForm

from app.models import Lab
from app.models import Role
from app.models import Request

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
			return redirect('/about')
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
