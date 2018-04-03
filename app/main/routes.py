from datetime import datetime
from flask import flash, render_template, redirect, request, url_for, \
    current_app
from flask_login import current_user, login_required
from app import db
from app.main.models import User
from app.main import bp


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    '''View function for the main index page.'''
    return render_template('index.html')
