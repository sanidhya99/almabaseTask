import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
import requests
import random
from django.conf import settings

def generate_otp_secret():
    return random.randint(1000, 9999)

def send_otp_via_call(mobile, otp):
    # Placeholder for sending OTP via SMS
    url = f"https://2factor.in/API/V1/{settings.APIKEY}/{mobile}/{otp}/Your 365 Alive OTP is"
    payload = ""
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.get(url, data=payload, headers=headers)
    if response.ok:
        return True
    else:
        return False