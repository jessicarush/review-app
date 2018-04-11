from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Length, Email
from app.main.models import Topic, Review
from app import create_app



def choices():
    app = create_app()
    with app.app_context():
        topics = Topic.query.order_by(Topic.filename).all()
        choices = [(t.filename, t.filename) for t in topics]
        return choices


class ReviewForm(FlaskForm):
    filename = SelectField('Topic:', choices=choices())
    time_spent = IntegerField('Time spent:', validators=[DataRequired()])
    skill_before = DecimalField('skill before:', places=1, validators=[DataRequired()])
    skill_after = DecimalField('skill after: ', places=1, validators=[DataRequired()])
    submit1 = SubmitField('Submit')


class DeleteReviewForm(FlaskForm):
    review_id = IntegerField('Review ID', validators=[DataRequired()])
    submit2 = SubmitField('Delete')


class DeleteTopicForm(FlaskForm):
    filename = SelectField('Topic:', choices=choices(), validators=[DataRequired()])
    submit3 = SubmitField('Delete')

class RenameTopicForm(FlaskForm):
    old_filename = SelectField('Old name:', choices=choices(), validators=[DataRequired()])
    new_filename = StringField('New name:', validators=[DataRequired()])
    submit4 = SubmitField('Rename')
