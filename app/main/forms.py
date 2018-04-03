from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length, Email


# class ExampleForm(FlaskForm):
#     post = TextAreaField('Say something', validators=[DataRequired(),
#         Length(min=1, max=280)])
#     submit = SubmitField('Post')
