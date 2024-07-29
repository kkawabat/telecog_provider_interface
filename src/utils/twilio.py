import os

from dotenv import load_dotenv
from twilio.rest import Client


load_dotenv()
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
sender_number = os.environ['SENDER_NUMBER']
client = Client(account_sid, auth_token)


def send_sms(receiver_number, body):
    message = client.api.account.messages.create(
        to=receiver_number,
        from_=sender_number,
        body=body)
    pass
