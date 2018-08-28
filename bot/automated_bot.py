# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# zapamti da su useri iz nekog razloga neaktivni pri sign-up !!!!!
import json
import requests
from random import randint

import string
import random

# from account.models import User


# url_for_signup = "http://127.0.0.1:8000/api/account/sign-up/"
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

    user = None
    password = None
    headers = None
    user_post_number = None
    posts = []

    def __init__(self):
        self.user_name = "user%s" % randint(1, 1000)
        self.user_post_number = randint(1, max_posts_per_user)
        self.user_mail = "%s@mail.com" % self.user_name
        self.password = pass_generator()

        pass

    def signup(self):
        # url = api_url + "account/signup/"
        data = {
            "username": self.user_name,
            "email": self.user_mail,
            "password": self.password
        }
        response = requests.post("%saccount/signup/" % api_url, data)
        response = json.loads(response.content.decode('utf-8'))
        self.user = response

    def login(self):
        # login_url = api_url + "account/login/"
        login = requests.post(
            "%saccount/login/" % api_url,
            {'username': self.user_name, 'password': self.password}
        )
        response = json.loads(login.content.decode('utf-8'))
        authorization = 'JWT ' + response['token']
        self.headers = {
            'Content-type': 'application/json',
            'Authorization': authorization
        }

    def create_post(self):
        for count in range(0, self.user_post_number):
            title = post_generator(10)
            text = post_generator(50)
            post_data = {
                "title": title,
                "text": text
            }
            post_data_json = json.dumps(post_data)
            response = requests.post(
                "%sentities/post/" % api_url,
                post_data_json,
                headers=self.headers
            )
            post = json.loads(response.content.decode('utf-8'))
            self.posts.append(post)


# !!! testing !!!

user = User()
user.signup()
user.login()
user.create_post()
print(user)
print(user.user)
print(user.password)
print(user.headers)
print(user.user_post_number)
print(user.posts)

# !!! testing !!!


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


users = []
for counter in range(1, number_of_users+1):
    '''
    Create users, get user authorization and create posts
    '''
    user = User()
    user.signup()
    user.login()
    user.create_post()
    users.append(user)

# sort users by number of posts
users_desent = users
users_desent.sort(key=lambda x: x.user_post_number, reverse=True)
for user in users:
    print(user.user_post_number)

for user in users_desent:
    print(user.user_post_number)
# for user in users:

# print(users)
# for user in users_desent:
#     if user:
#     print(user.user_post_number)


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

