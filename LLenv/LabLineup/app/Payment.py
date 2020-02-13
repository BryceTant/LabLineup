#Copyright 2020 LabLineup
#NOTE: The API Key is hardcoded and should be removed if the code is publicly published

from square.configuration import Configuration
from square.client import Client

from django.contrib.auth.models import User

import datetime
from pytz import utc as utc
from django.utils import timezone
from dateutil.relativedelta import relativedelta

ACCESS_TOKEN = "EAAAEKhuO_dB5OIb_klu9b6LC4Z8kyyGVK6CF6oOXHFwYFe5vQHDcMWEM4DidtaB"
ENV = "sandbox"
LOCATION = "CJ5PA0KHCQEA0"

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
            "idempotency_key": "PUT UNIQUE HERE",
            "order": {
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
            "ask_for_shipping_address": False,
            "merchant_support_email": "contact@lablineup.com",
            "pre_populate_buyer_email": str(user.email),
            "redirect_url": "https://www.lablineup.com/account"
        }
    )

    if result.is_success():
        return result.body["checkout"]["checkout_page_url"]
    elif result.is_error():
        return None
    else:
        return None

#To find the most recent payment for a subscription
def findPayment(subID):
    """Returns a tuple of product name and amount"""
    now = datetime.datetime.now(utc)
    result = sq.orders.search_orders(
        body = {
            "location_ids": [LOCATION],
            "query": {
                "filter": {
                    "date_time_filter": {
                        "created_at": {
                            "start_at": str(now - relativedelta(years=2)),
                            "end_at": str(now + relativedelta(days=1))
                        }
                    },
                },
                "sort": {
                    "sort_field": "CREATED_AT",
                    "sort_order": "DESC"
                }
            }
        }
    )

    if result.is_success():
        for order in results.body["orders"]:
            if order["reference_id"] == subID:
                orderAmt = order["tenders"][0]["amount_money"]["amount"]
                if orderAmt != 0:
                    return (order["line_items"][0]["name"], orderAmt)
        return (None, 0)
    elif result.is_error():
        print(result.errors)