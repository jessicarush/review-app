'''Blueprint for auth package of Review application.'''

from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.auth import routes
