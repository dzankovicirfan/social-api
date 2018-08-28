# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse

from rest_framework.test import APIClient, APITestCase

from .models import User


class UserTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='test',
            email='test@email.com',
            password='12345'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('api:account:user-list')

    def test_get_users_success(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_get_users_more_users_success(self):
        self.user1 = User.objects.create(
            username='test1',
            email='test1@email.com',
            password='123456'
        )
        self.user2 = User.objects.create(
            username='test2',
            email='test2@email.com',
            password='123456'
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_post_user_success(self):
        data = {
            'username': 'testko',
            'email': 'testko@email.com',
            'password': '12345'
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 2)

    def test_post_without_email_failed(self):
        data = {
            'username': 'testko',
            'password': '12345'
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 1)

    def test_post_wrong_email_failed(self):
        data = {
            'username': 'testko',
            'email': 'testkoemail.com',
            'password': '12345'
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 1)

    def test_signup_alredy_exist_failed(self):
        self.url = reverse('api:account:signup')

        data = {
            'username': 'test',
            'email': 'test@email.com',
            'password': '12345'
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 1)

    def test_signup_success(self):
        self.url = reverse('api:account:signup')

        data = {
            'username': 'test1',
            'email': 'test1@email.com',
            'password': '12345'
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 2)

    def test_login_success(self):
        self.url = reverse('api:account:login')
        self.user1 = User.objects.create(
            username='test1',
            email='test1@email.com',
            password='12345'
        )
        self.user1.set_password('12345')
        self.user1.save()
        response = self.client.post(self.url, {'username': 'test1', 'password': '12345'})

        self.assertEqual(response.status_code, 200)
