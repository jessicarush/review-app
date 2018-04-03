from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login


class User(UserMixin, db.Model):
    '''Model for the user table'''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return None
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Topic(db.Model):
    '''Model for study topic'''
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(64), index=True, unique=True)
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    current_skill = db.Column(db.Integer)
    mastery = db.Column(db.Integer)
    # one to many relationships:
    reviews = db.relationship('Review', backref='topic', lazy='dynamic')

    def __repr__(self):
        return '<Topic {}>'.format(self.filename)


class Review(db.Model):
    '''Model for review session'''
    id = db.Column(db.Integer, primary_key=True)
    review_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    before_skill = db.Column(db.Integer)
    after_skill = db.Column(db.Integer)
    # one to many relationship:
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))

    def __repr__(self):
        return '<Topic {}>'.format(self.filename)
