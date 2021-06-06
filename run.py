'''Start file for Review application.'''

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(port=5000, debug=False)
    # app.run('0.0.0.0', debug=True, port=5000, ssl_context='adhoc')
