# Review App

This is a small study tool built in Python & Flask that I created to help track and encourage study & review sessions. It is built to work with any number of github repositories containing files (topics) you want to study.

I started learning Python in 2017. Though I was keeping good notes in a github repo, I found that in absorbing so much new information everyday, it was hard to remember what I'd learned a week ago. This app was a way to organize and encourage myself to review the the notes I had written. To make it easier, the app recommends what topic I should review next based on the last time it was studied and my self-assessed comprehension of the topic.

If you would like to use this tool, you can use the [live version here at review.zebro.id](https://review.zebro.id/register) or you can instantiate your own copy of the application by following the instructions below.

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
$ git clone https://github.com/jessicarush/review-app.git
```

## Usage
Once you've got a copy of the application on your local machine, navigate to the the topmost `review/` directory.
This app requires [Python 3.6 or higher](https://www.python.org/downloads/).

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
<http://127.0.0.1:5000/register> to register yourself.

The app is designed to work with github, where a repository contains notes (files) on the topics you want to study. Ideally, the files we be named to reflect the topic like in [this repo on python](https://github.com/jessicarush/python-notes) or [this one on javascript](https://github.com/jessicarush/javascript-notes).

When you add a repository to the app and on login, it will check for any new topics (files from the repo). In adding a new topic it will want to know what you think your comprehension is on a scale of 0-5. Depending on the size of the repository, this initial set-up may feel tedious but any numbers you provide here will help the study recommendations.

Once you submit you should see a page showing you all the topics in the added repo. You can sort these topics by name, date-last-reviewed, or current skill. The *recommend* feature will suggest a topic for you to review next based on these three things.

The forms in the dark area allow you to add and remove study sessions, delete and rename topics. Note though, if you delete topics here, they will get added again next time you login unless they get removed from the repository.

This app has helped me to review and retain the things that I've learned. If it helps you too, let me know. Happy learning!

## Future Features

- [ ] Add heatmap
- [ ] Add help information
- [ ] Add 'make default' to repo list
- [ ] Add a dark theme
- [ ] remove .0 decimals from skill number


![Python Review App](/app/static/img/screenshot.png "Python Review App running in Firefox")
