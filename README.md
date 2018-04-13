# Review App

Work in progress...

- set up, activate venv
- install requirements
- set the flask variable: `$ export FLASK_APP=run.py`
- init database: `$ flask db init`
- migrate the database: `$ flask db migrate -m 'initial migrate'`
- build the db tables: `$ flask db upgrade`
- run: python run.py

initially there will be no users, so go to:
http://127.0.0.1:5003/auth/register

Once you've created an account, you can block the registration route by uncommenting `@login_required` at line 13 of app/auth/routes.py

Once you register, you'll be redirected to sign in.

This next part is going to suck. The app is programmed to check for newly added topics (files from the python repo) on login. In adding the new topic it will want to know what you think your understanding of this topic is on a scale of 0-5. The topics are links so you can check it out briefly if you want but I would suggest just going with your gut. At the time of this writing there were 90 topics. So that means 90 questions to answer. I timed myself on this and it took my approximately 15 minutes. 



Right now this it set up to only handle one user per database.
