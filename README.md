# Python Review App

This is a small Flask app I created to help me track my Python study & review sessions.

I started learning Python in 2017. Though I was keeping good notes, I found that in absorbing so much new information all the time, it was hard to remember what I'd done a weeks ago. This study app, was a way to organize myself in reviewing the topics I had learned. To make it easy, the app recommends what topic I should review next based on the last time it was reviewed and my self-assessed understanding of the topic.

If you would like to use this tool, follow the instructions below. Note that the app is built around reviewing the [Python notes in this repo](https://github.com/jessicarush/python-notes).

## Table of Contents

<!-- toc -->

- [Installation](#installation)
- [Usage](#usage)
  * [Set up a virtual environment](#set-up-a-virtual-environment)
  * [Install the requirements](#install-the-requirements)
  * [Set the flask environment variable](#set-the-flask-environment-variable)
  * [Create a *.env* file for the rest of your environment variables](#create-a-env-file-for-the-rest-of-your-environment-variables)
  * [Build the database](#build-the-database)
  * [Run the program](#run-the-program)

<!-- tocstop -->

## Installation
Clone or download:
```
$ git clone https://github.com/jessicarush/review.git
```

## Usage
Once you've got a copy of the application on your local machine, navigate to the the topmost `review/` directory.
This app requires [Python 3.5 or higher](https://www.python.org/downloads/).

### Set up a virtual environment
In the `review/` directory:
```
$ python3 -m venv venv
$ source venv/bin/activate
```

### Install the requirements

```
$ pip install -r requirements.txt
```

### Set the flask environment variable
```
$ export FLASK_APP=run.py
```

### Create a *.env* file for the rest of your environment variables

If you take a look at the `config.py` file, you'll see many of the variables are set to look for environment variables. This app uses [python-dotenv](https://github.com/theskumar/python-dotenv/blob/master/README.md) which means you can store these variables in a file named `.env` located in the same directory as `config.py`. The .env file can be used for all configuration-time variables, but it can't be used for Flask's FLASK_APP and FLASK_DEBUG environment variables because these are needed very early in the application process, before the app instance and its configuration object exist.

Here's an example `.env` for this project:

```
SECRET_KEY=your_supersecretpasswordkey
MAIL_SERVER=smtp.googlemail.com
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USERNAME=your_address@gmail.com
MAIL_PASSWORD=your_gmail_password
ADMIN=your_address@gmail.com
```

Note: This file isn't required to run the app. The email settings are used for sending password resets and server error logs. If you don't add these variables, those particular features won't work. If you choose to use your gmail account, you'll need to change your gmail settings to [allow less secure apps](https://support.google.com/accounts/answer/6010255?hl=en).

### Build the database
```
$ flask db upgrade
```

### Run the program
```
$ python run.py
```

Initially there will be no users, so go to:
<http://127.0.0.1:5003/register> to register yourself.

>Note: Once you've created an account, you can block the registration endpoint by uncommenting `@login_required` at line 14 of app/auth/routes.py

Once registered, you'll be directed to sign in.

This next part is going to require some patience. On login, the app is designed to check for any newly added topics (files from the python repo noted above). In adding a new topic it will want to know what you think your comprehension is on a scale of 0-5. The topics are links so you can check it out if you want but I would suggest just going with your gut. At the time of this writing there were 91 topics. So that means 91 questions to answer. I timed myself on this and it took approximately 15 minutes. If you'd rather start with a clean slate just tab 0's all the way down.

Once you submit you should see a page showing you all the topics. You can sort the topics by name, date-last-reviewed, or skill. The *recommend* feature will suggest a topic for you to review based on these three things.

The forms in the dark area allow you to add and remove study sessions from your database. Note though, if you delete topics here, they will get added again next time you login unless they get removed from the master repo.

This app is built for an individual: one user per database. Should you add another user via the register endpoint, they will be looking at the same database as you. Over the next year I will look at extending this to allow for multiple users in the same database.

Happy learning!

## Future Version Features

- [ ] Add heatmap
- [ ] Add help information
- [ ] Add 'make default' to repo list
- [ ] Add a dark theme
- [ ] remove .0 decimals from skill number


![Python Review App](/app/static/img/screenshot.png "Python Review App running in Firefox")
