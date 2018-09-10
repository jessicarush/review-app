'''Main view functions for Review application.'''

from datetime import datetime
# import os
from flask import flash, render_template, redirect, request, url_for, Markup
from flask_login import login_required
from wtforms import DecimalField
from wtforms.validators import NumberRange
from app import db
from app.main import bp
from app.main.forms import ReviewForm, DeleteReviewForm, DeleteTopicForm, \
    RenameTopicForm, AddTopicsForm
from app.main.models import Topic, Review
from app.main.topics import topics_from_repo, topics_from_db


@bp.route('/<sort_by>', methods=['GET', 'POST'])
@login_required
def index(sort_by='name'):
    '''View function for the main index page.'''
    review_form = ReviewForm()
    del_review_form = DeleteReviewForm()
    del_topic_form = DeleteTopicForm()
    rename_form = RenameTopicForm()

    topics = Topic.query.order_by(Topic.filename).all()
    choices = [(t.filename, t.filename) for t in topics]
    choices.insert(0, ('', '\u25b8  select a topic'))

    review_form.filename.choices = choices
    del_topic_form.filename.choices = choices
    rename_form.old_filename.choices = choices

    if review_form.submit1.data and review_form.validate_on_submit():
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

    if del_review_form.submit2.data and del_review_form.validate_on_submit():
        review = Review.query.filter_by(id=del_review_form.review_id.data).first()
        topic = Topic.query.filter_by(id=review.topic_id).first()
        if review.skill_after == int(5):
            topic.mastery -= 1
        Review.query.filter_by(id=del_review_form.review_id.data).delete()

        prev_review = Review.query.filter_by(topic_id=topic.id).order_by(
            Review.review_date.desc()).first()
        if prev_review:
            topic.current_skill = prev_review.skill_after
            topic.last_study_date = prev_review.review_date
        else:
            topic.current_skill = topic.start_skill
            topic.last_study_date = topic.created_date
        db.session.commit()
        flash('Review session deleted.')
        return redirect(url_for('main.index', sort_by='name'))

    if del_topic_form.submit3.data and del_topic_form.validate_on_submit():
        Topic.query.filter_by(filename=del_topic_form.filename.data).delete()
        db.session.commit()
        flash('Topic deleted.')
        return redirect(url_for('main.index', sort_by='name'))

    if rename_form.submit4.data and rename_form.validate_on_submit():
        topic = Topic.query.filter_by(filename=rename_form.old_filename.data).first()
        topic.filename = rename_form.new_filename.data
        db.session.commit()
        flash('Topic renamed!')
        return redirect(url_for('main.index', sort_by='name'))

    if sort_by == 'skill':
        topics = Topic.query.order_by(Topic.current_skill).all()
    elif sort_by == 'date':
        topics = Topic.query.order_by(Topic.last_study_date).all()
    else:
        topics = Topic.query.order_by(Topic.filename).all()
    return render_template(
        'index.html', topics=topics, review_form=review_form,
        del_review_form=del_review_form, del_topic_form=del_topic_form,
        rename_form=rename_form, recommend=request.args.get('recommend'))


@bp.route('/recommend')
@login_required
def recommend():
    '''View function to recommend a study topic.'''
    topics = Topic.query.order_by(Topic.last_study_date).limit(10).all()
    topics = sorted(topics, key=lambda x: x.current_skill)
    # flash('You should review {}'.format(topics[0].filename))
    url = '\"https://github.com/jessicarush/python-notes/blob/master/{}\"'.format(topics[0].filename)
    flash(Markup('You should review: <a href={} target="_blank">{}</a>'.format(url, topics[0].filename)))
    return redirect(url_for(
        'main.index', sort_by='date', recommend=topics[0].filename))


@bp.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    '''View for adding new topics.'''
    repo_filenames = set(topics_from_repo())
    db_filenames = set(topics_from_db())
    new_filenames = list(repo_filenames.difference(db_filenames))
    # new_field_names = [os.path.splitext(n)[0] for n in new_filenames]
    if not new_filenames:
        return redirect(url_for('main.index', sort_by='name'))

    class F(AddTopicsForm):
        '''Subclass to allow for dynamic number of form fields.'''
        pass

    for field_name in new_filenames:
        setattr(F, field_name, DecimalField(field_name, places=1, \
                validators=[NumberRange(min=0, max=5)]))

    form = F()

    if form.validate_on_submit():
        for field in form:
            if field.widget.input_type != 'hidden' and field.id != 'submit':
                print(field.id, field.data)
                topic = Topic(filename=field.id, start_skill=field.data,
                              current_skill=field.data)
                db.session.add(topic)
        db.session.commit()
        flash('New topic(s) added.')
        return redirect(url_for('main.index', sort_by='name'))
    return render_template('update.html', title='New Topics', form=form)


@bp.route('/demo/<sort_by>', methods=['GET', 'POST'])
def demo(sort_by='name'):
    '''View function for a DEMO of the main index page.'''
    review_form = ReviewForm()
    del_review_form = DeleteReviewForm()
    del_topic_form = DeleteTopicForm()
    rename_form = RenameTopicForm()

    topics = Topic.query.order_by(Topic.filename).all()
    choices = [(t.filename, t.filename) for t in topics]
    choices.insert(0, ('', '\u25b8  select a topic'))

    review_form.filename.choices = choices
    del_topic_form.filename.choices = choices
    rename_form.old_filename.choices = choices

    if review_form.submit1.data and review_form.validate_on_submit():
        flash("Sorry, 'Log a Study Session' has been disabled for this demo.")
        return redirect(url_for('main.demo', sort_by='name'))

    if del_review_form.submit2.data and del_review_form.validate_on_submit():
        flash("Sorry, 'Delete a Study Session' has been disabled for this demo.")
        return redirect(url_for('main.demo', sort_by='name'))

    if del_topic_form.submit3.data and del_topic_form.validate_on_submit():
        flash("Sorry, 'Delete a Topic' has been disabled for this demo.")
        return redirect(url_for('main.demo', sort_by='name'))

    if rename_form.submit4.data and rename_form.validate_on_submit():
        flash("Sorry, 'Rename a Topic' has been disabled for this demo.")
        return redirect(url_for('main.demo', sort_by='name'))

    if sort_by == 'skill':
        topics = Topic.query.order_by(Topic.current_skill).all()
    elif sort_by == 'date':
        topics = Topic.query.order_by(Topic.last_study_date).all()
    else:
        topics = Topic.query.order_by(Topic.filename).all()
    return render_template(
        'index.html', topics=topics, review_form=review_form,
        del_review_form=del_review_form, del_topic_form=del_topic_form,
        rename_form=rename_form, recommend=request.args.get('recommend'))


@bp.route('/demo_recommend')
def demo_recommend():
    '''View function to recommend a study topic on the DEMO route.'''
    topics = Topic.query.order_by(Topic.last_study_date).limit(10).all()
    topics = sorted(topics, key=lambda x: x.current_skill)
    flash('You should review {}'.format(topics[0].filename))
    return redirect(url_for('main.demo', sort_by='date', recommend=topics[0].filename))
