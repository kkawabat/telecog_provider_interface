import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def send_epsom_result(patient_name, patient_email, epsom_pdf):
    body = f"""Hello, {patient_name},

Thank you for completing the ePSOM survey, here is your personalized brain health plan. 

Linus Health    
"""
    email_params = {
        'subject': "ePSOM Brain Health Plan",
        'body': body,
        'sender_email': os.environ['SENDER_EMAIL'],
        'sender_password': os.environ['SENDER_EMAIL_PASSWORD'],
        'recipient_email': patient_email,
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 465,
        'attachments': [('epsom.pdf', epsom_pdf)]
    }
    send_email(email_params)


def send_email(email_params):
    message = MIMEMultipart()
    message['Subject'] = email_params['subject']
    message['From'] = email_params['sender_email']
    message['To'] = email_params['recipient_email']
    body_part = MIMEText(email_params['body'])
    message.attach(body_part)

    if 'attachments' in email_params:
        for file_name, data in email_params['attachments']:
            message.attach(MIMEApplication(data, Name=file_name))

    with smtplib.SMTP_SSL(email_params['smtp_server'], email_params['smtp_port']) as server:
        server.login(email_params['sender_email'], email_params['sender_password'])
        server.sendmail(email_params['sender_email'], email_params['recipient_email'], message.as_string())
