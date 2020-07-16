'''Authorization related forms for Review application.'''

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, \
  Length
from app.main.models import User


class RegistrationForm(FlaskForm):
    '''The registration form.'''
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

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


class LoginForm(FlaskForm):
    '''The login form.'''
    user_or_email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class ResetPasswordRequestForm(FlaskForm):
    '''The request password reset form.'''
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    submit = SubmitField('Request reset')


class ResetPasswordForm(FlaskForm):
    '''The reset password form.'''
    password = PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField('Save password')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    new_password = PasswordField('New password', validators=[DataRequired(),
                                 Length(min=4, max=60)])
    password_submit = SubmitField('Update password')


class EditLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=60)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    profile_submit = SubmitField('Save changes')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditLoginForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('That username is taken.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError('That email is already registered.')


class DeleteAccountForm(FlaskForm):
    user_or_email = StringField('Username or email',
                                validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    delete_submit = SubmitField('Delete account')
