from datetime import datetime
from flask import flash, render_template, redirect, request, url_for, \
    current_app
from flask_login import current_user, login_required
from app import db
from app.main.models import User, Topic, Review
from app.main import bp
from app.main.topics import get_topics_from_repo


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    '''View function for the main index page.'''
    # topics = get_topics_from_repo()
    return render_template('index.html')


# @bp.route('/update', methods=['GET', 'POST'])
# @login_required
# def update_topics():
#     # form = UpdateTopicsForm()
#     # if form.validate_on_submit():
#     topic = Topic(filename=, created_date=, current_skill=)
