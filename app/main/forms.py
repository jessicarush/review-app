'''Main forms for modifying the database.'''

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class ReviewForm(FlaskForm):
    '''Form for entering review session data.'''
    filename = SelectField('Topic:', choices=[])
    time_spent = IntegerField('Time spent:', validators=[DataRequired()])
    skill_before = DecimalField(
        'skill before:', places=1, validators=[NumberRange(min=0, max=5)])
    skill_after = DecimalField(
        'skill after:', places=1, validators=[NumberRange(min=0, max=5)])
    submit1 = SubmitField('Submit')


class DeleteReviewForm(FlaskForm):
    '''Form for a deleting review session.'''
    review_id = IntegerField('Review ID', validators=[DataRequired()])
    submit2 = SubmitField('Delete')


class DeleteTopicForm(FlaskForm):
    '''Form for deleting a topic.'''
    filename = SelectField('Topic:', choices=[], validators=[DataRequired()])
    submit3 = SubmitField('Delete')


class RenameTopicForm(FlaskForm):
    '''Form for renaming a topic.'''
    old_filename = SelectField('Old name:', choices=[], validators=[DataRequired()])
    new_filename = StringField('New name:', validators=[DataRequired()])
    submit4 = SubmitField('Rename')


class AddTopicsForm(FlaskForm):
    '''Form for adding new topics.'''
    # fields are generated dynamically in the /update route
    submit = SubmitField('Submit')
