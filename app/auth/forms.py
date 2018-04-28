'''Authorization related forms for Review application.'''

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.main.models import User


class LoginForm(FlaskForm):
    '''The login form.'''
    user_or_email = StringField('Username or email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class ResetPasswordRequestForm(FlaskForm):
    '''The request password reset form.'''
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request reset')


class ResetPasswordForm(FlaskForm):
    '''The reset password form.'''
    password = PasswordField('New Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Save password')


class RegistrationForm(FlaskForm):
    '''The registration form.'''
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        '''Check that the username does't already exist.'''
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('That username is taken.')

    def validate_email(self, email):
        '''Check that the email does't already exist.'''
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('That email is already registered.')
