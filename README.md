# SOCIAL-API


### Installation

Install the dependencies.

```sh
$ cd social-api
$ virtualenv v
$ source v/Script/activate
$ cd socialapi
$ pip install -r requirements.txt
$ python manage.py migrate
```

### Run tests
```sh
$ python manage.py tests
```

### Run server
```sh
$ python manage.py runserver
```

### Run bot
Run server before running a bot.
```sh
$ cd social-api/bot
$ python automated_bot.py
```
