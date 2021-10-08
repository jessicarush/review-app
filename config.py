'''Config file for application.'''

import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config():
    '''Config class for application.'''

    PROJECT_NAME = 'Review'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Extend csrf token expirey to 1 week
    # Note: If set to None, the CSRF token is valid for the life of the session
    WTF_CSRF_TIME_LIMIT = 3600 * 24 * 7

    # To address cookie security
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True

    # For sending emails:
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # For receiving emailed error log, contact emails:
    ADMINS = [os.environ.get('ADMIN')]

    # The api url for a github repo containing files to be studied:
    API_START = 'https://api.github.com/repos/'
    API_END = '/contents'

    # The url for particular file in a repo:
    URL_START = 'https://github.com/'
    URL_END = '/blob/master/'

    # Repo API url should look like:
    # https://api.github.com/repos/jessicarush/python-notes/contents

    # Repo urls look like:
    # https://github.com/jessicarush/python-notes

    # File urls look like:
    # https://github.com/jessicarush/python-notes/blob/master/classes.py
