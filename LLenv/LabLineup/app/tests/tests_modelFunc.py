"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

import datetime
from pytz import utc as utc
import django
from django.test import TestCase
import app.modelFunc as mf

from django.contrib.auth.models import User
from app.models import Lab
from app.models import Role
from app.models import Request
from app.models import LabCode
from app.models import Notify
from app.models import PasswordResetCode
from app.models import Subscription
from app.models import EmailConfirmation


class ModelFuncTest(TestCase):
    #User Objects
    User0 = None
    User1 = None
    User2 = None
    User3 = None
    #Lab Objects
    Lab0 = None
    Lab1 = None
    #Lab Codes, Not LabCode objects
    LabCode0 = None
    LabCode1 = None
    LabCode2 = None
    LabCode3 = None
    #Subscription Objects
    Sub0 = None
    Sub1 = None
    Sub2 = None
    Sub3 = None
    #Request Objects
    Request0 = None
    Request1 = None
    Request2 = None
    Request3 = None
    Request4 = None
    Request5 = None
    Request6 = None
    Request7 = None
    Request8 = None
    Request9 = None

    def setUp(self):
        #  Set up Users  --------------------------------------------------

        self.User0 = User.objects.create_user(username="testUsername0",
                                             email = "test0@test.com",
                                             password = None,
                                             first_name = "Test First 0",
                                             last_name = "Test Last 0")
        self.User0.set_password("testPassword0")
        self.User0.save()

        self.User1 = User.objects.create_user(username="testUsername1",
                                             email = "test1@test.com",
                                             password = None,
                                             first_name = "Test First 1",
                                             last_name = "Test Last 1")
        self.User1.set_password("testPassword1")
        self.User1.save()

        self.User2 = User.objects.create_user(username="testUsername2",
                                             email = "test2@test.com",
                                             password = None,
                                             first_name = "Test First 2",
                                             last_name = "Test Last 2")
        self.User2.set_password("testPassword2")
        self.User2.save()

        self.User3 = User.objects.create_user(username="testUsername3",
                                             email = "test3@test.com",
                                             password = None,
                                             first_name = "Test First 3",
                                             last_name = "Test Last 3")
        self.User3.set_password("testPassword3")
        self.User3.save()

        #  Set up Labs  ---------------------------------------------------

        self.Lab0 = Lab.objects.create(name="Test Lab 0",
                                  description="This is Test Lab 0")
        self.Lab1 = Lab.objects.create(name="Test Lab 1",
                                  description="This is Test Lab 1")

        #  Set up LabCodes  -----------------------------------------------
        #  This tests generateLabCode
        self.LabCode0 = mf.generateLabCode(self.Lab0.lid, 's') #Student code for Lab0
        self.LabCode1 = mf.generateLabCode(self.Lab0.lid, 't') #TA code for Lab0
        self.LabCode2 = mf.generateLabCode(self.Lab1.lid, 's') #Student code for Lab1
        self.LabCode3 = mf.generateLabCode(self.Lab1.lid, 't') #TA code for Lab1

        #  Set up Subscriptions  ------------------------------------------
        self.Sub0 = Subscription.objects.create(uid_id=self.User0.id,
                                                initialSub = datetime.datetime.now(utc),
                                                subRenewal = datetime.datetime.now(utc),
                                                labLimit = 123)
        self.Sub1 = Subscription.objects.create(uid_id=self.User1.id,
                                                initialSub = datetime.datetime.now(utc),
                                                subRenewal = datetime.datetime.now(utc),
                                                labLimit = 5)
        self.Sub2 = Subscription.objects.create(uid_id=self.User2.id,
                                                initialSub = datetime.datetime.now(utc),
                                                subRenewal = datetime.datetime.now(utc),
                                                labLimit = 1)
        self.Sub3 = Subscription.objects.create(uid_id=self.User3.id,
                                                initialSub = datetime.datetime.now(utc),
                                                subRenewal = datetime.datetime.now(utc),
                                                labLimit = 321)

        #   Set up Requests
        self.Request0 = Request.objects.create(rid = 1,
                                               station = 000,
                                               description = "Request description 0",
                                               timeSubmitted = datetime.datetime.now(utc),
                                               timeCompleted = None,
                                               feedback = None,
                                               suid = self.User0,
                                               lid = self.Lab0,
                                               huid = self.User1,
                                               complete=False)
        self.Request1 = Request.objects.create(rid = 2,
                                               station = 111,
                                               description = "Request description 1",
                                               timeSubmitted = datetime.datetime.now(utc),
                                               timeCompleted = datetime.datetime.now(utc),
                                               feedback = None,
                                               suid = self.User0,
                                               lid = self.Lab0,
                                               huid = self.User1,
                                               complete=True)
        self.Request2 = Request.objects.create(rid = 3,
                                               station = 222,
                                               description = "Request description 2",
                                               timeSubmitted = datetime.datetime.now(utc),
                                               timeCompleted = datetime.datetime.now(utc),
                                               feedback = None,
                                               suid = self.User1,
                                               lid = self.Lab1,
                                               huid = self.User2,
                                               complete=True)
        self.Request3 = Request.objects.create(rid = 4,
                                               station = 333,
                                               description = "Request description 3",
                                               timeSubmitted = datetime.datetime.now(utc),
                                               timeCompleted = None,
                                               feedback = None,
                                               suid = self.User1,
                                               lid = self.Lab1,
                                               huid = self.User2,
                                               complete=False)
        self.Request4 = Request.objects.create(rid = 5,
                                               station = 444,
                                               description = "Request description 4",
                                               timeSubmitted = datetime.datetime.now(utc),
                                               timeCompleted = datetime.datetime.now(utc),
                                               feedback = None,
                                               suid = self.User1,
                                               lid = self.Lab1,
                                               huid = self.User3,
                                               complete=True)
        self.Request5 = Request.objects.create(rid = 6,
                                               station = 555,
                                               description = "Request description 5",
                                               timeSubmitted = datetime.datetime.now(utc),
                                               timeCompleted = datetime.datetime.now(utc),
                                               feedback = None,
                                               suid = self.User1,
                                               lid = self.Lab1,
                                               huid = self.User2,
                                               complete=True)
        self.Request6 = Request.objects.create(rid = 7,
                                               station = 665,
                                               description = "Request description 6",
                                               timeSubmitted = datetime.datetime.now(utc),
                                               timeCompleted = None,
                                               feedback = None,
                                               suid = self.User1,
                                               lid = self.Lab1,
                                               huid = self.User3,
                                               complete=False)
        self.Request7 = Request.objects.create(rid = 8,
                                               station = 777,
                                               description = "Request description 7",
                                               timeSubmitted = datetime.datetime.now(utc),
                                               timeCompleted = None,
                                               feedback = None,
                                               suid = self.User1,
                                               lid = self.Lab1,
                                               huid = None,
                                               complete=False)
        self.Request8 = Request.objects.create(rid = 9,
                                               station = 888,
                                               description = "Request description 8",
                                               timeSubmitted = datetime.datetime.now(utc),
                                               timeCompleted = None,
                                               feedback = None,
                                               suid = self.User1,
                                               lid = self.Lab1,
                                               huid = None,
                                               complete=False)
        self.Request9 = Request.objects.create(rid = 10,
                                               station = 999,
                                               description = "Request description 9",
                                               timeSubmitted = datetime.datetime.now(utc),
                                               timeCompleted = None,
                                               feedback = None,
                                               suid = self.User1,
                                               lid = self.Lab1,
                                               huid = None,
                                               complete=False)
        #   set up Roles
        self.Role0 = Role.objects.create(lid = self.Lab0,
                                            uid = self.User0,
                                            role = 'p')

        self.Role1 = Role.objects.create(lid = self.Lab1,
                                            uid = self.User1,
                                            role = 's')

        self.Role2 = Role.objects.create(lid = self.Lab1,
                                            uid = self.User2,
                                            role = 't')


    def test_getLabCode(self):
        self.assertNotEqual("3ff93",
                            mf.getLabCode(self.Lab0.lid, 's'))
        self.assertNotEqual(self.LabCode0, self.LabCode1)
        self.assertEqual(self.LabCode0,
                         mf.getLabCode(self.Lab0.lid, 's'))
        self.assertEqual(self.LabCode1,
                         mf.getLabCode(self.Lab0.lid, 't'))
        self.assertEqual(self.LabCode2,
                         mf.getLabCode(self.Lab1.lid, 's'))
        self.assertEqual(self.LabCode3,
                         mf.getLabCode(self.Lab1.lid, 't'))

    def test_deleteLabCode(self):
        mf.deleteLabCode(self.LabCode0)
        mf.deleteLabCode(self.LabCode3)

        self.assertEqual(None, mf.getLabCode(self.Lab0.lid, 's'))
        self.assertEqual(None, mf.getLabCode(self.Lab1.lid, 't'))

        self.assertNotEqual(self.LabCode0, mf.getLabCode(self.Lab0.lid, 's'))
        self.assertNotEqual(self.LabCode3, mf.getLabCode(self.Lab1.lid, 't'))

    def test_getLabLimit(self):
        self.assertNotEqual("0", mf.getLabLimit(self.User0.id))
        self.assertNotEqual(40, mf.getLabLimit(self.User1.id))
        self.assertNotEqual(0, mf.getLabLimit(self.User2.id))
        self.assertNotEqual(None, mf.getLabLimit(self.User3.id))

        self.assertEqual(123, mf.getLabLimit(self.User0.id))
        self.assertEqual(5, mf.getLabLimit(self.User1.id))
        self.assertEqual(1, mf.getLabLimit(self.User2.id))
        self.assertEqual(321, mf.getLabLimit(self.User3.id))
    
    def test_getUserByEmail(self):
        self.assertNotEqual(None, mf.getUserByEmail("test0@test.com"))
        self.assertNotEqual(self.User1, mf.getUserByEmail("test0@test.com"))
        self.assertNotEqual(None, mf.getUserByEmail("test1@test.com"))
        self.assertNotEqual(self.User2, mf.getUserByEmail("test1@test.com"))
        self.assertNotEqual(None, mf.getUserByEmail("test2@test.com"))
        self.assertNotEqual(self.User3, mf.getUserByEmail("test2@test.com"))
        self.assertNotEqual(None, mf.getUserByEmail("test3@test.com"))
        self.assertNotEqual(self.User0, mf.getUserByEmail("test3@test.com"))

        self.assertEqual(self.User0, mf.getUserByEmail("test0@test.com"))
        self.assertEqual(self.User1, mf.getUserByEmail("test1@test.com"))
        self.assertEqual(self.User2, mf.getUserByEmail("test2@test.com"))
        self.assertEqual(self.User3, mf.getUserByEmail("test3@test.com"))
    
    def test_getNumComplete(self):
        self.assertNotEqual(None, mf.getNumComplete(self.Lab0.lid))
        self.assertNotEqual(-1, mf.getNumComplete(self.Lab0.lid))
        self.assertNotEqual(None, mf.getNumComplete(self.Lab1.lid))
        self.assertNotEqual(-1, mf.getNumComplete(self.Lab1.lid))

        self.assertEqual(1, mf.getNumComplete(self.Lab0.lid))
        self.assertEqual(3, mf.getNumComplete(self.Lab1.lid))

    def test_getNumCompleteTA(self):
        self.assertNotEqual(None, mf.getNumCompleteTA(self.Lab0.lid, self.User1))
        self.assertNotEqual(0, mf.getNumCompleteTA(self.Lab0.lid, self.User1))
        self.assertNotEqual(None, mf.getNumCompleteTA(self.Lab1.lid, self.User2))
        self.assertNotEqual(0, mf.getNumCompleteTA(self.Lab1.lid, self.User2))

        self.assertEqual(1, mf.getNumCompleteTA(self.Lab0.lid, self.User1))
        self.assertEqual(2, mf.getNumCompleteTA(self.Lab1.lid, self.User2))
        self.assertEqual(1, mf.getNumCompleteTA(self.Lab1.lid, self.User3))
    
    def test_getNameOfUser(self):
        self.assertNotEqual(None, mf.getNameOfUser(self.User0.id))
        self.assertNotEqual(None, mf.getNameOfUser(self.User1.id))
        self.assertNotEqual(None, mf.getNameOfUser(self.User2.id))
        self.assertNotEqual(None, mf.getNameOfUser(self.User3.id))

        self.assertEqual("Test First 0 Test Last 0", mf.getNameOfUser(self.User0.id))
        self.assertEqual("Test First 1 Test Last 1", mf.getNameOfUser(self.User1.id))
        self.assertEqual("Test First 2 Test Last 2", mf.getNameOfUser(self.User2.id))
        self.assertEqual("Test First 3 Test Last 3", mf.getNameOfUser(self.User3.id))

    def test_generatePasswordResetCode(self):
        self.assertNotEqual(None, mf.generatePasswordResetCode(self.User0.id))
        self.assertNotEqual(None, mf.generatePasswordResetCode(self.User1.id))
        self.assertNotEqual(None, mf.generatePasswordResetCode(self.User2.id))
        self.assertNotEqual(None, mf.generatePasswordResetCode(self.User3.id))

    def test_resetPasswordFunc(self):
        self.assertEqual(1,1)
    
    def test_removeLabFromAccount(self):
        self.assertNotEqual(self.Role1, mf.removeLabFromAccount(self.User0.id, self.Lab0.lid))
        self.assertEqual(False, mf.removeLabFromAccount(self.User0.id, self.Lab0.lid))

        self.assertNotEqual(self.Role1, mf.removeLabFromAccount(self.User1.id, self.Lab1.lid))
        self.assertEqual(False, mf.removeLabFromAccount(self.User1.id, self.Lab1.lid))

        self.assertNotEqual(self.Role1, mf.removeLabFromAccount(self.User2.id, self.Lab1.lid))
        self.assertEqual(False, mf.removeLabFromAccount(self.User2.id, self.Lab1.lid))
    
    def test_getOutstandingRequests(self):
        self.assertNotEqual(None, mf.getOutstandingRequest(self.Lab0.lid, self.User1.id))
        self.assertEqual(self.Request0, mf.getOutstandingRequest(self.Lab0.lid, self.User1.id))

        self.assertNotEqual(None, mf.getOutstandingRequest(self.Lab1.lid, self.User2.id))
        self.assertEqual(self.Request3, mf.getOutstandingRequest(self.Lab1.lid, self.User2.id))

        self.assertNotEqual(None, mf.getOutstandingRequest(self.Lab1.lid, self.User3.id))
        self.assertEqual(self.Request6, mf.getOutstandingRequest(self.Lab1.lid, self.User3.id))
        