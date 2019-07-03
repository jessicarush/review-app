'''Models for Review app database tables.'''

from datetime import datetime
import requests
from time import time

from flask import current_app
from flask_login import UserMixin, current_user
import jwt
from sqlalchemy import extract
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class User(UserMixin, db.Model):
    '''Model for the user table'''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # review_count = db.Column(db.Integer)
    # one to many relationship:
    repos = db.relationship('Repo', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        '''Generates a password hash.'''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        '''Checks that the password matches that hash.'''
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        '''Returns a password reset token.'''
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        '''Verifies the token to allow a password reset.'''
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return None
        return User.query.get(id)


@login.user_loader
def load_user(id):
    '''Helper function for Flask-Login.'''
    return User.query.get(int(id))


class Repo(db.Model):
    '''Model for the main topic (a github repo)'''
    id = db.Column(db.Integer, primary_key=True)
    repository = db.Column(db.String(128))
    # many to one relationship:
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # one to many relationship:
    topics = db.relationship('Topic', backref='repo', lazy='dynamic')

    @staticmethod
    def ping_repo(repo):
        '''Verifies the that a repo exists on github.'''
        url = current_app.config['API_START'] + repo + current_app.config['API_END']
        response = requests.get(url)
        if response.status_code == 200:
            return True


class Topic(db.Model):
    '''Model for study topic'''
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(64), index=True)
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_study_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    start_skill = db.Column(db.Float, default=0)
    current_skill = db.Column(db.Float, index=True)
    mastery = db.Column(db.Integer, default=0)
    # many to one relationship:
    repo_id = db.Column(db.Integer, db.ForeignKey('repo.id'))
    # one to many relationship:
    reviews = db.relationship('Review', backref='topic', lazy='dynamic')

    @staticmethod
    def recommend_study_topic(selected_repo):
        '''Recommend a study topic from a repo.'''
        try:
            # How many topics are 20% (rounded)
            count = Topic.query.filter_by(repo_id=selected_repo.id).count()
            count = round(count * .2) if round(count * .2) else 1

            # Get the (count) oldest topics
            topics = Topic.query.filter_by(repo_id=selected_repo.id) \
                                .order_by(Topic.last_study_date) \
                                .limit(count).all()

            # Check if a search by the oldest date yields a greater count:
            y = topics[0].last_study_date.year
            m = topics[0].last_study_date.month
            d = topics[0].last_study_date.day
            t = Topic.query.filter(Topic.repo_id == selected_repo.id,
                                   extract('year', Topic.last_study_date) == y,
                                   extract('month', Topic.last_study_date) == m,
                                   extract('day', Topic.last_study_date) == d).all()
            if len(t) > count:
                topics = t

            # sort by current_skill
            topics = sorted(topics, key=lambda x: x.current_skill)
            recommend = topics[0].filename
        except:
            recommend = None
        finally:
            return recommend


class Review(db.Model):
    '''Model for review session'''
    id = db.Column(db.Integer, primary_key=True)
    review_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    time_spent = db.Column(db.Integer)
    skill_before = db.Column(db.Float)
    skill_after = db.Column(db.Float)
    # many to one relationship:
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
