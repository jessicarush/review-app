from flask import current_app
import requests


def get_topics_from_repo():
    url = current_app.config['API_URL']
    response = requests.get(url)
    # print('Status code:', response.status_code)
    r = response.json()
    t = [i['name'] for i in r if i['type'] == 'file' and i['name'] != 'README.md']
    return t
