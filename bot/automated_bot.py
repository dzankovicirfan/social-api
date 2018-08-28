# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# zapamti da su useri iz nekog razloga neaktivni pri sign-up !!!!!
import json
import requests
from random import randint

import string
import random

# from account.models import User


# url_for_sign_up = "http://127.0.0.1:8000/api/account/sign-up/"
# url_for_login = "http://127.0.0.1:8000/api/account/login/"
# url_for_posting = "http://127.0.0.1:8000/api/entities/post/"
# url_for_like = "http://127.0.0.1:8000/api/entities/like/"

def load_config():
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
        return data


config = load_config()

api_url = config['api_url']
number_of_users = config['number_of_users']
max_posts_per_user = config['max_posts_per_user']
max_likes_per_user = config['max_likes_per_user']


def post_generator(length):
    # generating title and text for post
    return ''.join(random.choice(string.ascii_letters) for m in range(length))


def pass_generator(size=6, char=string.ascii_uppercase + string.digits):
    # random passwords for user
    return ''.join(random.choice(char) for _ in range(size))


class User(object):

    def __init__(self):
        self.user = None
        self.password = None
        self.headers = None
        self.user_post_number = None
        self.post = []

    def sign_up(self, counter):
        url = api_url + "account/sign-up/"
        user_name = "user" + "%s" % counter
        self.user_post_number = randint(0, max_posts_per_user)
        user_mail = user_name + "@mail.com"
        password = pass_generator()
        data = {
            "username": user_name,
            "email": user_mail,
            "password": password,
            "is_active": True
        }
        response = requests.post(url, data)
        response = json.loads(response.content.decode('utf-8'))
        self.user = response
        self.password = password

    def login(self):
        login_url = api_url + "account/login/"
        login = requests.post(
            login_url,
            {'username': self.user['username'], 'password': self.password}
        )
        response = json.loads(login.content.decode('utf-8'))
        authorization = 'JWT ' + response['token']
        self.headers = {
            'Content-type': 'application/json',
            'Authorization': authorization
        }

    def create_post(self):
        url = api_url + "entities/post/"
        for count in range(1, self.user_post_number+1):
            title = post_generator(10)
            text = post_generator(50)
            post_data = {
                "title": title,
                "text": text,
                "user": self.user['id']
            }
            post_data_json = json.dumps(post_data)
            response = requests.post(url, post_data_json, headers=self.headers)
            post = json.loads(response.content.decode('utf-8'))
            self.post.append(post)



def find_post(users):
    return


def liking(user, post_id):
    '''
    when post is found, like it
    '''
    url = api_url + "entities/like/"

    data = {
        "post": post_id,
        "user": user['id']
    }
    json_data = json.dumps(data)
    requests.post(url, json_data, headers=user.headers)
    user['likes_NO'] += 1
    user.save()
    return

# user = User()
# user.sign_up(24)
# user.login()
# user.create_post()

users = []
for counter in range(1, number_of_users+1):
    '''
    Create users, get user authorization and create posts
    '''
    user = User()
    user.sign_up(counter)
    user.login()
    user.create_post()
    users.append(user)

#sort users by number of posts
users.sort(key=lambda x: x.user_post_number, reverse=True)
# for user in users:

print(users)
for user in users:
    if user
    print(user.user_post_number)
#     # check
# print(users)
#     #creating posts
#     create_posts(user['id'], headers, user_post_number)
#     #check
#     #liking
# ## user to like is user with most post, that didn't reach max likes


# ## user is liking until he reaches max likes
# for count in range(user_like, max_likes_per_user):
#     like(post)


# ## user can like only post from user that has post with 0 likes


# ## stop when every post has a like
# ## can not like it's own post


# ## post can be liked more times but by differen users

