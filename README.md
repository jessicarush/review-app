# Review App

This is a small Flask app I created to help me track my Python study & review sessions.

I started learning Python in 2017. Though I was keeping good notes, I found that in absorbing so much new information all the time, it was hard to remember what I'd done 2 weeks ago. This study app, was a way to organize myself in reviewing the topics I had learned. To make it easy, the app recommends what topic I should review next based on the last time it was reviewed and my self-assessed understanding of the topic.

If you would like to use this tool, follow the instructions below. Note that the app is built around reviewing the [Python notes in this repo](https://github.com/jessicarush/python-examples).

## Clone or download
```
$ git clone https://github.com/jessicarush/review.git
```

## Set up a virtual environment
Make sure you're in the topmost *review/* directory first:
```
$ python3 -m venv venv
$ source venv/bin/activate
```

## Install the requirements
```
$ pip install -r requirements.txt
```

## Set the flask environment variable
```
$ export FLASK_APP=run.py
```

## Build the database
```
$ flask db upgrade
```

## Run the program
```
$ python run.py
```

Initially there will be no users, so go to:
<http://127.0.0.1:5003/auth/register> to register yourself.

>Note: Once you've created an account, you can block the registration endpoint by uncommenting `@login_required` at line 14 of app/auth/routes.py

Once registered, you'll be directed to sign in.

This next part is going to require some patience. On login, the app is designed to check for any newly added topics (files from the python repo noted above). In adding a new topic it will want to know what you think your understanding is on a scale of 0-5. The topics are links so you can check it out if you want but I would suggest just going with your gut. At the time of this writing there were 91 topics. So that means 91 questions to answer. I timed myself on this and it took approximately 15 minutes. If you'd rather start with a clean slate just tab 0's all the way down.

Once you submit you should see a page showing you all the topics. You can sort the topics by name, date-last-reviewed, or skill. The *recommend* feature will suggest a topic for you to review based on these three things.

The forms in the dark area allow you to add and remove study sessions from your database. Note though, if you delete topics here, they will get added again next time you login unless they get removed from the master repo.

This app is built for an individual: one user per database. Should you add another user via the register endpoint, they will be looking at the same database as you. Over the next year I will look at extending this to allow for multiple users in the same database.

Happy learning!
