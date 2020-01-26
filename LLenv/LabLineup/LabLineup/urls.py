"""
Definition of urls for LabLineup.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views


urlpatterns = [
    path('', views.home, name='home'),  #Home page of website
    path('contact/', views.contact, name='contact'),  #Contact form/information page
    path('about/', views.about, name='about'),  #About page with info on app
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
         name='login'),  #Login page
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),  #Logout page
    path('register/', views.register, name='register'),  #Create an account page
    path('admin/', admin.site.urls),  #Admin panel
	path('help/', views.help, name='help'),  #Help and FAQs page
	path('app/', views.selectLab, name='selectLab'),  #First page of app (select a lab)
    path('createLab/', views.createLab, name='createLab'),  #Page to create a new lab (as professor)
	path('addLab/', views.addLab, name='addLab'),  #Page to add a lab to your account (using a lab code)
	path('student/request/', views.studentRequest, name='studentRequest'),  #Student page for lab to submit a new request
	path('student/requestSubmitted/', views.studentRequestSubmitted, name='studentRequestSubmitted'),  #Student page after request submitted (waiting page)
	path('student/requestFeedback/', views.studentRequestFeedback, name='studentRequestFeedback'),  #Student page after request has been completed (feedback)
    path('student/requestHistory/', views.requestHistory, name='requestHistory'), #To view submitted requests
	path('lab/queue/', views.labQueue, name='labQueue'),  #TA/Professor queue for the lab
	path('lab/queue/currentRequest', views.currentRequest, name='currentRequest'), #TA/Professor responding to request
	path('lab/manageLab/', views.labManage, name='labManage'),  #Page to manage lab settings
	path('lab/feedback/', views.labFeedback, name='labFeedback'),  #Professor page to view feedback and select TA's to view feedback
	path('lab/feedback/helper/', views.labFeedbackHelper, name='labFeedbackHelper'),  #Professor/TA page to view the TA's feedback
	path('professor/', views.professor, name='professor'),  #Professor page to select between manageLab, manageNotifications, feedback, etc.
	path('ta/', views.ta, name='ta'),  #TA page to select between manageNotifications, feedback for TA, etc.
	path('account/', views.manageAccount, name='manageAccount'),  #Manage account page (to change name, email, password, etc.)
	path('account/resetPassword/<str:prc>/', views.resetPassword, name='resetPassword'), #View to accept new password if prc (password reset code) is found
	path('account/forgotPassword/', views.forgotPassword, name='forgotPassword'), #View to all user to enter user
    path('account/requestEmailConfirmation/', views.requestEmailConfirmation, name='requestEmailConfirmation'), #To request a new email confirm to be sent
    path('account/confirmAccount/<str:regConCode>/', views.confirmAccountView, name='confirmAccountView'), #View to confirm new account
]
