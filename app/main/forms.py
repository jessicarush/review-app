from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Length, Email, NumberRange


class ReviewForm(FlaskForm):
    filename = SelectField('Topic:', choices=[])
    time_spent = IntegerField('Time spent:', validators=[DataRequired()])
    skill_before = DecimalField('skill before:', places=1, validators=[NumberRange(min=0, max=5)])
    skill_after = DecimalField('skill after:', places=1, validators=[NumberRange(min=0, max=5)])
    submit1 = SubmitField('Submit')


class DeleteReviewForm(FlaskForm):
    review_id = IntegerField('Review ID', validators=[DataRequired()])
    submit2 = SubmitField('Delete')


class DeleteTopicForm(FlaskForm):
    filename = SelectField('Topic:', choices=[], validators=[DataRequired()])
    submit3 = SubmitField('Delete')


class RenameTopicForm(FlaskForm):
    old_filename = SelectField('Old name:', choices=[], validators=[DataRequired()])
    new_filename = StringField('New name:', validators=[DataRequired()])
    submit4 = SubmitField('Rename')


class AddTopicsForm(FlaskForm):
    # fields are generated dynamically in the /update route
    submit = SubmitField('Submit')
