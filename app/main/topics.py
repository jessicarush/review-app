'''Functions for getting repo topics.'''

from flask import current_app
import requests
from app import create_app
from app.main.models import Topic


def topics_from_repo(repository):
    '''Collects all the filenames from a given Github repo.'''
    api_start = current_app.config['API_START']
    api_end = current_app.config['API_END']
    api = api_start + repository + api_end
    response = requests.get(api)
    # print(api)
    # print('Status code:', response.status_code)
    r = response.json()

    def filter_topics(i):
        if i['type'] != 'file' or i['name'][0] == '.' or i['name'] == 'README.md':
            return False
        return True

    topics = [i['name'] for i in r if filter_topics(i)]
    return topics


def topics_from_database(repo_id):
    '''Collects all the filenames from the database to compare against repo.'''
    app = create_app()
    with app.app_context():
        topics = Topic.query.filter_by(repo_id=repo_id).order_by(Topic.filename).all()
        t = [t.filename for t in topics]
    return t
