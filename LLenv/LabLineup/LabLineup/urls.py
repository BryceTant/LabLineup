"""
Definition of urls for LabLineup.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register, name='register'),
    path('admin/', admin.site.urls),
	path('help/', views.help, name='help'),
	path('app/', views.selectLab, name='selectLab'),
    path('createLab/', views.createLab, name='createLab'),
	path('addLab/', views.addLab, name='addLab'),
	path('lab/<int:labID>/student/', views.labStudent, name='labStudent'),
	path('lab/<int:labID>/queue/', views.labQueue, name='labQueue'),
	path('lab/<int:labID>/manageLab/', views.labManage, name='labManage'),
	path('lab/<int:labID>/feedback/', views.labFeedback, name='labFeedback'),
	path('lab/<int:labID>/feedback/<int:helperID>/', views.labFeedbackHelper, name='labFeedbackHelper'),
]
