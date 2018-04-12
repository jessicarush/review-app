from flask import current_app
import requests
from app import create_app
from app.main.models import Topic


def topics_from_repo():
    url = current_app.config['API_URL']
    response = requests.get(url)
    # print('Status code:', response.status_code)
    r = response.json()
    t = [i['name'] for i in r if i['type'] == 'file' and i['name'] != 'README.md']
    return t


def topics_from_db():
    app = create_app()
    with app.app_context():
        topics = Topic.query.order_by(Topic.filename).all()
        t = [t.filename for t in topics]
    return t


def topic_choices():
    app = create_app()
    with app.app_context():
        topics = Topic.query.order_by(Topic.filename).all()
        t = [(t.filename, t.filename) for t in topics]
    return t
