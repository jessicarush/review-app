'''Authorization related email functions for Review application.'''

from flask import render_template, current_app
from app.main.email import send_email


def send_password_reset_email(user):
    '''Sends an email with a link to reset password.'''
    token = user.get_reset_password_token()
    send_email(current_app.config['PROJECT_NAME'] + ': Password Reset',
               # sender=current_app.config['ADMINS'][0],
               sender=current_app.config['HOSTNAME_EMAIL'],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
