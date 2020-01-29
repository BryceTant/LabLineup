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