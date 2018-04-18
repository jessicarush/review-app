'''Blueprint for main package of Review application.'''

from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes
