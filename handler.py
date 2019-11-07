import os
import json

import arrow
import requests
from twilio.rest import Client

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM = os.environ.get("TWILIO_FROM", "")

PHONE_NUMBER = "+18016736421"
SLC = 'Salt+Lake+Hardware+Building+Management'
HOME = '15227+Drumbeat+Ln,+Bluffdale,+UT+84065'
URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={}&destinations={}&key={}&departure_time={}'

##
# 7 - 5 in UTC
#
PREFERRED_TIMES = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

ICONS = {
    'racecar': '🏎️',
    'car': '🚗',
    'stopsign': '🛑',
}

def is_weekday():
    """
    :return boolean: true if current day is weekday
    """
    WEEKDAYS =  [1, 2, 3, 4, 5]
    return arrow.utcnow().weekday() in WEEKDAYS

def is_weekend():
    """
    :return boolean: true if current day is weekend
    """
    WEEKENDS =  [0, 6]
    return arrow.utcnow().weekday() in WEEKENDS

def send_message(message, number):
    """
    sends formatted message to twilio

    :param message: string
    :param number: string
    """
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    data = {"body": message, "to": number, "from_": TWILIO_FROM}
    client.messages.create(**data)

def notify(event, context):
    """
    AWS Lambda entry point

    :param event: (unused) event from AWS Lambda
    :param context: (unused) context from AWS Lambda
    """
    hour = arrow.utcnow().hour
    day = arrow.utcnow().weekday()

    if is_weekend() or hour not in PREFERRED_TIMES:
        return

    departure_time = arrow.utcnow().timestamp
    response = requests.get(URL.format(SLC, HOME, GOOGLE_API_KEY, departure_time)).json()
    travel_time = response["rows"][0]["elements"][0]["duration_in_traffic"]["text"]
    icon = ICONS["car"]
    message = f"Current travel time home is {travel_time} {icon}"
    send_message(message, PHONE_NUMBER)


if __name__ == "__main__":
    notify('', '')
