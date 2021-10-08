'''Blueprint for errora package of Review application.'''

from flask import Blueprint

bp = Blueprint('errors', __name__)

from app.errors import handlers
