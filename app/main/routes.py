'''Main view functions for Review application.'''

from datetime import datetime
import re

from flask import current_app, flash, render_template, redirect, request, \
    url_for, Markup
from flask_login import current_user, login_required
from sqlalchemy import extract
from wtforms.fields.html5 import DecimalField
from wtforms.validators import NumberRange

from app import db
from app.main import bp
from app.main.forms import ReviewForm, DeleteReviewForm, DeleteTopicForm, \
    RenameTopicForm, AddTopicsForm, AddRepoForm, DeleteRepoForm
from app.main.models import User, Repo, Topic, Review
from app.main.topics import topics_from_repo, topics_from_database


@bp.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    '''View for checking for and adding new topics.'''

    class F(AddTopicsForm):
        '''Subclass to allow for dynamic form fields.'''
        pass

    base_url = current_app.config['URL_START']
    repos = current_user.repos.all()
    new_repo = request.args.get('new_repo')
    new_topics = None
    file_count = 0

    # If the user has no existing repos (a new user), send them back to index:
    if not repos:
        return redirect(url_for('main.index', sort='name'))

    # If the user just added a new repo:
    elif new_repo:
        new_topics = topics_from_repo(new_repo)
        if not new_topics:
            return redirect(url_for('main.index', sort='name'))
        else:
            for t in new_topics:
                t_count = t + '_' + str(file_count)
                setattr(F, t_count, DecimalField(t, description=new_repo))
                file_count += 1

    # Otherwise run a check to see if there are any new topics in any repo:
    else:
        # get a list of the users repositories:
        repositories = [r.repository for r in repos]
        # for each repo get the topics from github and compare to the database:
        for r in repositories:
            repo = Repo.query.filter(Repo.repository == r,
                                     Repo.user_id == current_user.id).first()
            github_topics = topics_from_repo(repo.repository)
            database_topics = topics_from_database(repo.id)
            new_topics = set(github_topics).difference(set(database_topics))
            # if there are new topics, add these to the dynamic form
            if new_topics:
                # in case two or more topics from different repos have
                # the same name, append a number (which will be removed
                # when we receive the form data.
                for t in new_topics:
                    t_count = t + '_' + str(file_count)
                    setattr(F, t_count, DecimalField(t, description=repo.repository))
                    file_count += 1

        # if there are no new topics, proceed to main.index
        if not new_topics:
            return redirect(url_for('main.index', sort='name'))

    form = F()

    # process forms:
    if form.validate_on_submit():
        for field in form:
            if field.widget.input_type != 'hidden' and field.id != 'add_topic_submit':
                # print(field.id, field.data, field.description)
                repo = Repo.query.filter(Repo.repository == field.description,
                                         Repo.user_id == current_user.id).first()

                # remove the file_count off of the field.id
                filename = re.sub(r'_\d*\b', '', field.id)

                topic = Topic(filename=filename, start_skill=field.data,
                              current_skill=field.data, repo_id=repo.id)
                db.session.add(topic)
        db.session.commit()
        flash('New topic(s) added.', category='main-success')
        return redirect(url_for('main.index',
                                selected_repo=repo.repository,
                                sort='name'))

    return render_template('update.html',
                           title='New Topics',
                           form=form,
                           new_repo=new_repo,
                           base_url=base_url,
                           new_topics=new_topics)


@bp.route('/<sort>', methods=['GET', 'POST'])
@login_required
def index(sort='name'):
    '''View function for the main index page.'''

    add_repo_form = AddRepoForm()
    review_form = ReviewForm()
    del_review_form = DeleteReviewForm()
    del_topic_form = DeleteTopicForm()
    rename_topic_form = RenameTopicForm()
    del_repo_form = DeleteRepoForm()

    repos = current_user.repos.all()
    topics = None
    recommend = None
    base_url = None
    file_url = None
    add_repo_messages = None
    selected_repo = Repo.query.filter(
        Repo.repository == request.args.get('selected_repo'),
        Repo.user_id == current_user.id).first()

    # if there are repos but none has been selected, default to the first:
    if repos and not selected_repo:
        selected_repo = Repo.query.filter_by(user_id=current_user.id).first()

    if selected_repo:
        # build the base url to link to files:
        base_url = current_app.config['URL_START']
        url_end = current_app.config['URL_END']
        file_url = f'{base_url}{selected_repo.repository}{url_end}'

        # get the topics for display:
        if sort == 'skill':
            topics = Topic.query.filter_by(repo_id=selected_repo.id).order_by(Topic.current_skill).all()
        elif sort == 'date':
            topics = Topic.query.filter_by(repo_id=selected_repo.id).order_by(Topic.last_study_date).all()
        else:
            topics = Topic.query.filter_by(repo_id=selected_repo.id).order_by(Topic.filename).all()

        # build select menus for forms:
        form_topics = Topic.query.filter_by(repo_id=selected_repo.id).order_by(Topic.filename).all()
        topic_choices = [(t.filename, t.filename) for t in form_topics]
        topic_choices.insert(0, ('', ''))
        repo_choices = [(r.repository, r.repository) for r in repos]
        repo_choices.insert(0, ('', ''))

        review_form.filename.choices = topic_choices
        del_topic_form.filename.choices = topic_choices
        rename_topic_form.old_filename.choices = topic_choices
        del_repo_form.repository.choices = repo_choices

        # recommend a topic:
        recommend = Topic.recommend_study_topic(selected_repo)

    # process forms
    if add_repo_form.add_repo_submit.data and add_repo_form.validate_on_submit():
        # check that the repo exists on github and hasn't already beed added:
        reponame = add_repo_form.repository.data
        ping = Repo.ping_repo(reponame)
        repo = Repo.query.filter(Repo.repository == reponame,
                                 Repo.user_id == current_user.id).first()

        if not ping:
            flash("I couldn't find that repository on Github", category='main-fail')
            add_repo_messages = True
        elif repo:
            flash("You've added that one already", category='main-fail')
            add_repo_messages = True
        else:
            repo = Repo(repository=reponame, user_id=current_user.id)
            db.session.add(repo)
            db.session.commit()
            flash('New repository sucessfully added!', category='main-success')
            # direct to add update
            return redirect(url_for('main.update', new_repo=reponame))

    if review_form.review_submit.data and review_form.validate_on_submit():
        topic = Topic.query.filter(Topic.repo_id == selected_repo.id,
                                   Topic.filename == review_form.filename.data).first()
        review = Review(time_spent=review_form.time_spent.data,
                        skill_before=review_form.skill_before.data,
                        skill_after=review_form.skill_after.data,
                        topic_id=topic.id)
        topic.current_skill = review_form.skill_after.data
        topic.last_study_date = datetime.utcnow()
        if topic.current_skill == 5:
            topic.mastery += 1
        db.session.add(review)
        db.session.commit()
        flash('Review logged!', category='main-success')
        return redirect(url_for('main.index',
                                sort='name',
                                selected_repo=selected_repo.repository))

    if del_topic_form.del_topic_submit.data and del_topic_form.validate_on_submit():
        topic = Topic.query.filter(Topic.repo_id == selected_repo.id,
                                   Topic.filename == del_topic_form.filename.data).first()
        topic.reviews.delete()    # for query delete
        db.session.delete(topic)  # for single query result
        db.session.commit()
        flash('Topic deleted.', category='main-success')
        return redirect(url_for('main.index',
                                sort='name',
                                selected_repo=selected_repo.repository))

    if rename_topic_form.rename_submit.data and rename_topic_form.validate_on_submit():
        topic = Topic.query.filter(Topic.repo_id == selected_repo.id,
                                   Topic.filename == rename_topic_form.old_filename.data).first()
        topic.filename = rename_topic_form.new_filename.data
        db.session.commit()
        flash('Topic renamed!', category='main-success')
        return redirect(url_for('main.index',
                                sort='name',
                                selected_repo=selected_repo.repository))

    if del_repo_form.del_repo_submit.data and del_repo_form.validate_on_submit():
        repo = Repo.query.filter(Repo.user_id == current_user.id,
                                 Repo.repository == del_repo_form.repository.data).first()
        for t in repo.topics.all():
            t.reviews.delete()
        repo.topics.delete()
        db.session.delete(repo)
        db.session.commit()
        flash('Repo deleted', category='main-success')
        return redirect(url_for('main.index',
                                sort='name',
                                selected_repo=selected_repo.repository))












    #
    # if del_review_form.submit2.data and del_review_form.validate_on_submit():
    #     review = Review.query.filter_by(id=del_review_form.review_id.data).first()
    #     topic = Topic.query.filter_by(id=review.topic_id).first()
    #     if review.skill_after == int(5):
    #         topic.mastery -= 1
    #     Review.query.filter_by(id=del_review_form.review_id.data).delete()
    #
    #     prev_review = Review.query.filter_by(topic_id=topic.id).order_by(
    #         Review.review_date.desc()).first()
    #     if prev_review:
    #         topic.current_skill = prev_review.skill_after
    #         topic.last_study_date = prev_review.review_date
    #     else:
    #         topic.current_skill = topic.start_skill
    #         topic.last_study_date = topic.created_date
    #     db.session.commit()
    #     flash('Review session deleted.')
    #     return redirect(url_for('main.index', sort='name'))
    #


    # return render_template(
    #     'index.html', topics=topics, review_form=review_form,
    #     del_review_form=del_review_form, del_topic_form=del_topic_form,
    #     rename_form=rename_form, recommend=request.args.get('recommend'))
    return render_template('index.html',
                           sort=sort,
                           repos=repos,
                           topics=topics,
                           selected_repo=selected_repo,
                           recommend=recommend,
                           base_url=base_url,
                           file_url=file_url,
                           add_repo_messages=add_repo_messages,
                           add_repo_form=add_repo_form,
                           review_form=review_form,
                           del_review_form=del_review_form,
                           del_topic_form=del_topic_form,
                           rename_topic_form=rename_topic_form,
                           del_repo_form=del_repo_form)
