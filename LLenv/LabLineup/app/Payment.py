#Copyright 2020 LabLineup
#NOTE: The API Key is hardcoded and should be removed if the code is publicly published

from square.configuration import Configuration
from square.client import Client

from django.contrib.auth.models import User
from django.conf import settings

import datetime
from pytz import utc as utc
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import uuid

ACCESS_TOKEN = settings.SQUARE_ACCESS_TOKEN
ENV = settings.SQUARE_ENV
LOCATION = settings.SQUARE_LOCATION
BASE_ADDR = settings.BASE_URL

sq = Client(access_token=ACCESS_TOKEN, environment=ENV)

#To create a new customer. Returns None if fails
def createCustomer(userID):
    user = User.objects.get(id=userID)
    newCust = sq.customers.create_customer(
        {
            "given_name": user.first_name,
            "family_name": user.last_name,
            "email_address": user.email,
            "reference_id": user.id
        }
    )
    if newCust.is_success():
        return newCust.body["customer"]["id"]
    else:
        return None

#To get a link for the user to use to pay
def createCheckout(userID, subID, plan):
    """Plans: 0=Free, 1=Silver, 2=Gold"""
    user = User.objects.get(id=userID)
    planName = "LabLineup"
    planPrice = 0
    if plan == 1:
        planName = "LabLineup Silver"
        planPrice = 2000
    elif plan == 2:
        planName = "LabLineup Gold"
        planPrice = 3000
    result = sq.checkout.create_checkout(
        location_id = LOCATION,
        body = {
            "idempotency_key": uuid.uuid4().hex,
            "order": {
                "order": {
                    "location_id": LOCATION,
                    "reference_id": str(subID),
                    "line_items": [
                        {
                            "name": planName,
                            "quantity": "1",
                            "base_price_money": {
                                "amount": planPrice,
                                "currency": "USD"
                            }
                        },
                            ],
                        },
                },
            "ask_for_shipping_address": False,
            "merchant_support_email": "contact@lablineup.com",
            "pre_populate_buyer_email": str(user.email),
            "redirect_url": (BASE_ADDR + "/subscriptionConfirmation/")
        }
    )
    if result.is_success():
        return result.body["checkout"]["checkout_page_url"]
    elif result.is_error():
        return None
    else:
        return None

#To find the most recent payment for a subscription
def findRecentPayment(subID):
    """Returns a product name and order/transaction ID"""
    now = datetime.datetime.now(utc)
    startDate = (now - relativedelta(years=1, days=1)).isoformat()
    endDate = (now + relativedelta(days=1)).isoformat()
    result = sq.orders.search_orders(
        body = {
            "location_ids": [LOCATION],
            "query": {
                "filter": {
                    "date_time_filter": {
                        "created_at": {
                            "start_at": str(startDate),
                            "end_at": str(endDate)
                        }
                    },
                    "state_filter": {
                        "states": [
                            "COMPLETED"
                        ]
                    }
                },
                "sort": {
                    "sort_field": "CREATED_AT",
                    "sort_order": "DESC"
                }
            }
        }
    )

    if result.is_success() and result.body != {}:
        for order in result.body["orders"]:
            if order["reference_id"] == str(subID):
                orderAmt = order["tenders"][0]["amount_money"]["amount"]
                if orderAmt != 0:
                    return (order["line_items"][0]["name"], order["id"])
        return (None, None)
    else:
        return (None, None)

#To find which product was ordered by order/transaction ID
def findProductOrder(orderID):
    """Returns a product name and order/transaction ID"""
    result = sq.orders.search_orders(
        body = {
            "location_ids": [LOCATION],
            "query": {
                "filter": {
                    "state_filter": {
                        "states": [
                            "COMPLETED"
                        ]
                    }
                }
            }
        }
    )

    if result.is_success() and result.body != {}:
        for order in result.body["orders"]:
            if order["id"] == orderID:
                orderAmt = order["tenders"][0]["amount_money"]["amount"]
                if orderAmt != 0:
                    return (order["line_items"][0]["name"])
        return None
    else:
        return None