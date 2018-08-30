# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# zapamti da su useri iz nekog razloga neaktivni pri sign-up !!!!!
import json
import requests
from random import randint

import string
import random


def load_config():
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
        return data


config = load_config()

api_url = config['api_url']
number_of_users = config['number_of_users']
max_posts_per_user = config['max_posts_per_user']
max_likes_per_user = config['max_likes_per_user']


class User(object):

    user = None
    password = None
    headers = None
    user_post_number = None

    def __init__(self):
        self.username = "user%s" % self.pass_generator(12)
        self.user_post_number = randint(1, max_posts_per_user)
        self.user_mail = "%s@mail.com" % self.username
        self.password = self.pass_generator()

    @staticmethod
    def pass_generator(size=6, char=string.ascii_uppercase + string.digits):
        # random password for user
        return ''.join(random.choice(char) for _ in range(size))

    @staticmethod
    def post_generator(length):
        # generating title and text for post
        return ''.join(random.choice(string.ascii_letters) for m in range(length))

    def signup(self):
        data = {
            "username": self.username,
            "email": self.user_mail,
            "password": self.password
        }
        response = requests.post("%saccount/signup/?bot=1" % api_url, data)
        if response.status_code == 201:
            response = json.loads(response.content)

            self.user = response

    def login(self):
        response = requests.post(
            "%saccount/login/" % api_url,
            {'username': self.username, 'password': self.password}
        )
        response = json.loads(response.content)
        authorization = 'JWT %s' % response['token']
        self.headers = {
            'Content-type': 'application/json',
            'Authorization': authorization
        }

    def create_post(self):
        for count in range(0, self.user_post_number):
            title = self.post_generator(10)
            text = self.post_generator(50)
            post_data = {
                "title": title,
                "text": text
            }
            post_data_json = json.dumps(post_data)
            requests.post(
                "%sentities/post/" % api_url,
                post_data_json,
                headers=self.headers
            )

    def user_number_likes(self):
        response = requests.get("%sentities/like/?user=%s" % (api_url, self.user['id']), headers=self.headers)
        likes = len(json.loads(response.content))
        return likes

    def get_posts_from_other(self, users):
        users_filter = map(
            lambda x: 'user=%s' % x.user['id'],
            filter(lambda u: u.user['id'] != self.user['id'], users)
        )
        users_filter = '&'.join(users_filter)
        response = requests.get(
            "%sentities/post/?%s" % (api_url, users_filter),
            headers=self.headers
        )
        return json.loads(response.content)

    def like(self, post):
        '''
        when post is found, like it
        '''

        data = {
            "post": post['id']
        }
        json_data = json.dumps(data)
        requests.post("%sentities/like/" % api_url, json_data, headers=self.headers)
        return


def find_post_to_like(posts):
    zero_like_posts = list(filter(lambda x: len(x['likes']) == 0, posts))
    if len(zero_like_posts) == 0:
        return False
    users_pks = list(set(map(lambda x: x['user'], zero_like_posts)))
    users_posts = list(filter(lambda x: x['user'] in users_pks, posts))

    return random.choice(users_posts) if users_posts else None


def create_users_and_posts():
    users = []

    for counter in range(0, number_of_users):
        '''
        Create users, get user authorization and create posts
        '''
        user = User()
        user.signup()
        user.login()
        user.create_post()
        users.append(user)

    return users


def run_liking(users):
    i = 0
    # sort users by number of posts
    users_decending = sorted(users, key=lambda x: x.user_post_number, reverse=True)
    for user in users_decending:
        while user.user_number_likes() < max_likes_per_user:
            posts = user.get_posts_from_other(users)
            random_post = find_post_to_like(posts)
            if random_post is False:
                break
            if random_post:
                print('%s - liking random post: %s' % (
                    user.user['username'], random_post))
                i += 1
                user.like(random_post)
    print('Liked %s posts' % i)


def run_bot():
    users = create_users_and_posts()
    run_liking(users)


run_bot()
