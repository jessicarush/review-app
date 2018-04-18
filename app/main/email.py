'''Functions for sending emails in a new thread.'''

from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail


def send_asynchronous(app, msg):
    '''Create a custom application context for a new thread.'''
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    '''Send email ina new thread.'''
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_asynchronous,
           args=(current_app._get_current_object(), msg)).start()
