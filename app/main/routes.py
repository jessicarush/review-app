from datetime import datetime
from flask import flash, render_template, redirect, request, url_for, \
    current_app
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.main.forms import ReviewForm, DeleteReviewForm, DeleteTopicForm, \
    RenameTopicForm
from app.main.models import User, Topic, Review
from app.main.topics import topics_from_repo




@bp.route('/<sort_by>', methods=['GET', 'POST'])
# @bp.route('/index/<sort_by>', methods=['GET', 'POST'])
@login_required
def index(sort_by='name'):
    '''View function for the main index page.'''
    review_form = ReviewForm()
    del_review_form = DeleteReviewForm()
    del_topic_form = DeleteTopicForm()
    rename_form = RenameTopicForm()

    if review_form.validate_on_submit():
        topic = Topic.query.filter_by(filename=review_form.filename.data).first()
        review = Review(time_spent=review_form.time_spent.data,
                        skill_before=review_form.skill_before.data,
                        skill_after=review_form.skill_after.data,
                        topic_id=topic.id)
        topic.current_skill = review_form.skill_after.data
        topic.last_study_date = datetime.utcnow()
        if topic.current_skill == int(5):
            topic.mastery += 1
        db.session.add(review)
        db.session.commit()
        flash('Review logged!')
        return redirect(url_for('main.index', sort_by='name'))

    if del_review_form.validate_on_submit():
        Review.query.filter_by(id=del_review_form.review_id.data).delete()
        db.session.commit()
        flash('Review session deleted.')

    if del_topic_form.validate_on_submit():
        Topic.query.filter_by(filename=del_topic_form.filename).delete()
        db.session.commit()
        flash('Topic deleted.')

    if rename_form.validate_on_submit():
        topic = Topic.query.filter_by(filename=rename_form.old_filename).first()
        topic.filename = rename_form.new_filename.data
        db.session.commit()
        flash('Topic renamed!')

    if sort_by == 'skill':
        topics=Topic.query.order_by(Topic.current_skill).all()
    elif sort_by == 'date':
        topics=Topic.query.order_by(Topic.last_study_date).all()
    else:
        topics = Topic.query.order_by(Topic.filename).all()
    return render_template('index.html', topics=topics,
        review_form=review_form, del_review_form=del_review_form,
        del_topic_form=del_topic_form, rename_form=rename_form)


@bp.route('/recommend')
@login_required
def recommend():
    '''View function to recommend a study topic.'''
    # TODO: recommend function
    flash('You should study...')
    return redirect(url_for('main.index', sort_by='date'))
















# @bp.route('/update', methods=['GET', 'POST'])
# @login_required
# def update_topics():
#     # form = UpdateTopicsForm()
#     # if form.validate_on_submit():
    # topic = Topic(filename='ajax_notes.md', created_date=datetime(2018, 3, 26), current_skill=3)
    # db.session.add(topic)
    # db.session.commit()
    # flash('New topic(s) added.')
