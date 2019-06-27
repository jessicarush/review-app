'''Authorization view functions for Review application.'''

from flask import flash, render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordForm, \
    ResetPasswordRequestForm
from app.main.models import User
from app.auth.email import send_password_reset_email


@bp.route('/register', methods=['GET', 'POST'])
def register():
    '''View for registering a new user.'''

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # login ther new user
        login_user(user, remember='true')
        return redirect(url_for('main.update'))
    return render_template('auth/register.html', title='Register', form=form)

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/login', methods=['GET', 'POST'])
def login():
    '''View for logging in a user.'''

    if current_user.is_authenticated:
        return redirect(url_for('main.index', sort='name'))
    form = LoginForm()
    if form.validate_on_submit():
        # check if field is an existing username:
        user = User.query.filter_by(username=form.user_or_email.data).first()
        # check if field is an existing email:
        if user is None:
            user = User.query.filter_by(email=form.user_or_email.data).first()
        # if not found by username or email:
        if user is None:
            flash("Can't find that username or email.", category='auth-fail')
            return redirect(url_for('auth.login'))
        # if the username is good but password fails:
        if user and not user.check_password(form.password.data):
            flash('Incorrect password.', category='auth-fail')
            return redirect(url_for('auth.login'))
        # otherwise, all is well:
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.update'))
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    '''View for logging out a user.'''
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    '''View for requesting a password reset.'''
    if current_user.is_authenticated:
        return redirect(url_for('main.index', sort='name'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the link to reset your password.',
              category='auth-success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    '''View for resetting password.'''
    if current_user.is_authenticated:
        return redirect(url_for('main.index', sort='name'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index', sort='name'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.', category='auth-success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
