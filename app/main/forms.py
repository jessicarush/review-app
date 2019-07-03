'''Main forms for modifying the database.'''

import re

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.html5 import IntegerField, DecimalField
from wtforms.validators import DataRequired, NumberRange, ValidationError

# NOTE: NumberRange validators don't seem to be working. Added manually.


class ReviewForm(FlaskForm):
    '''Form for entering review session data.'''
    filename = SelectField('Log a study session', choices=[])
    time_spent = IntegerField('For how long (mins)?', validators=[DataRequired()])
    skill_before = DecimalField(
        'Skill before', places=1, validators=[NumberRange(min=0, max=5)])
    skill_after = DecimalField(
        'Skill after', places=1, validators=[NumberRange(min=0, max=5)])
    review_submit = SubmitField('Log review')


class DeleteReviewForm(FlaskForm):
    '''Form for a deleting review session.'''
    review_id = IntegerField('Delete study session', validators=[DataRequired()])
    del_review_submit = SubmitField('Delete session')


class DeleteTopicForm(FlaskForm):
    '''Form for deleting a topic.'''
    filename = SelectField('Delete topic', choices=[], validators=[DataRequired()])
    del_topic_submit = SubmitField('Delete topic')


class DeleteRepoForm(FlaskForm):
    '''Form for deleting a repository.'''
    repository = SelectField('Delete repository', choices=[], validators=[DataRequired()])
    del_repo_submit = SubmitField('Delete repository')


class RenameTopicForm(FlaskForm):
    '''Form for renaming a topic.'''
    old_filename = SelectField('Rename topic', choices=[], validators=[DataRequired()])
    new_filename = StringField('New name', validators=[DataRequired()])
    rename_submit = SubmitField('Rename topic')

    def validate_new_filename(self, new_filename):
        '''Check that the repository looks right in terms of format.'''
        # check that string contains only
        # alphanumeric, hyphen, underscore or period
        valid = re.match(r'^[-._\w]+$', new_filename.data) is not None
        if not valid:
            raise ValidationError("Names can contain alphanumeric, "
                                  "hyphens, underscores and periods.")


class AddTopicsForm(FlaskForm):
    '''Form for adding new topics.'''
    # fields are generated dynamically in the /update route
    add_topic_submit = SubmitField('Add topics')


class AddRepoForm(FlaskForm):
    '''Form for adding new repositories.'''
    repository = StringField('Add repository', validators=[DataRequired()])
    add_repo_submit = SubmitField('Add repository')

    def validate_repository(self, repository):
        '''Check that the repository looks right in terms of format.'''
        # check that string contains only alphanumeric, hyphen or forwardslash
        valid = re.match(r'^[-/\w]+$', repository.data) is not None
        if not valid:
            raise ValidationError("This should contain only alphanumeric "
                                  "characters, hyphens and a forward slash")
        # check that it follows the format: username/repository
        repo = repository.data.split('/')
        # if len(str(repository).split('/')) != 2:
        if len(repo) != 2 or '' in repo:
            raise ValidationError("Something doesn't look right. "
                                  "Your entry should look like: username/repository")
