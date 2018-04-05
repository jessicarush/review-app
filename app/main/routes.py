from datetime import datetime
from flask import flash, render_template, redirect, request, url_for, \
    current_app
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.main.models import User, Topic, Review
from app.main.topics import get_topics_from_repo

import shelve


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    '''View function for the main index page.'''
    # topics = get_topics_from_repo()
    topics = Topic.query.order_by(Topic.filename).all()
    return render_template('index.html', topics=topics)


@bp.route('/sort_by_skill', methods=['GET', 'POST'])
@login_required
def sort_by_skill():
    '''View function for the main index page, sorted by current skill.'''
    # topics = get_topics_from_repo()
    topics=Topic.query.order_by(Topic.current_skill).all()
    return render_template('index.html', topics=topics)


@bp.route('/sort_by_date', methods=['GET', 'POST'])
@login_required
def sort_by_date():
    '''View function for the main index page, sorted by current skill.'''
    # topics = get_topics_from_repo()
    topics=Topic.query.order_by(Topic.last_study_date).all()
    return render_template('index.html', topics=topics)


# topics = Topic.query.order_by(Topic.filename).all()
# for topic in topics:
#     mastery = 0
#     for review in topic.reviews:
#         if review.skill_after == 5.0:
#             mastery += 1
#     topic.mastery = mastery
# db.session.commit()


# review = Review(review_date=review_date,
#                 time_spent=time_spent,
#                 skill_before=skill_before,
#                 skill_after=skill_after,
#                 topic_id=topic.id)
# db.session.add(review)
# flash('New topic(s) added.')
# db.session.commit()


# @bp.route('/update', methods=['GET', 'POST'])
# @login_required
# def update_topics():
#     # form = UpdateTopicsForm()
#     # if form.validate_on_submit():
    # topic = Topic(filename='ajax_notes.md', created_date=datetime(2018, 3, 26), current_skill=3)
    # db.session.add(topic)
    # db.session.commit()
    # flash('New topic(s) added.')
