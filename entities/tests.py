# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse

from rest_framework.test import APIClient, APITestCase

from .models import Post, Like
from account.models import User


class PostTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='test',
            email='test@email.com'
        )
        self.user.set_password('12345')
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('api:entities:post-list')

    def test_get_success(self):
        self.post1 = Post.objects.create(
            title='First post',
            text='Some text',
            user=self.user
        )
        self.post1 = Post.objects.create(
            title='Second post',
            text='Some text',
            user=self.user
        )
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_create_post_success(self):
        data = {
            'title': 'First post',
            'text': 'Some text'
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user'], self.user.id)

    def test_update_post_success(self):
        self.post1 = Post.objects.create(
            title='First post',
            text='Some text',
            user=self.user
        )
        self.url = reverse('api:entities:post-detail', kwargs={'pk': self.post1.pk})

        data = {
            'title': 'Change title',
            'text': 'New text'
        }
        response = self.client.put(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Change title')
        self.assertEqual(response.data['text'], 'New text')

    def test_update_wrong_owner_failed(self):
        self.user1 = User.objects.create(
            username='test1',
            email='test1@email.com'
        )
        self.post1 = Post.objects.create(
            title='First post',
            text='Some text',
            user=self.user1
        )

        self.url = reverse('api:entities:post-detail', kwargs={'pk': self.post1.pk})

        data = {
            'title': 'Change title',
            'text': 'New text'
        }
        response = self.client.put(self.url, data)

        self.assertEqual(response.status_code, 400)

    def test_delete_success(self):
        self.post1 = Post.objects.create(
            title='First post',
            text='Some text',
            user=self.user
        )
        self.url = reverse('api:entities:post-detail', kwargs={'pk': self.post1.pk})

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, None)
        self.assertEqual(Post.objects.count(), 0)

    def test_delete_now_owner_failed(self):
        self.user1 = User.objects.create(
            username='test1',
            email='test1@email.com'
        )
        self.post1 = Post.objects.create(
            title='First post',
            text='Some text',
            user=self.user1
        )

        self.url = reverse('api:entities:post-detail', kwargs={'pk': self.post1.pk})

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Post.objects.count(), 1)


class LikeTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(
            username='test1',
            email='test1@email.com'
        )
        self.user1.set_password('12345')
        self.user1.save()

        self.user2 = User.objects.create(
            username='test2',
            email='test2@mail.com'
        )
        self.user1.set_password('12345')
        self.user1.save()

        self.post1 = Post.objects.create(
            title='First Post',
            text='Post from user1',
            user=self.user1
        )

        self.post2 = Post.objects.create(
            title='Second Post',
            text='Post from user2',
            user=self.user2
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)
        self.url = reverse('api:entities:like-list')

    def test_get_like_success(self):
        self.like1 = Like.objects.create(
            post=self.post1,
            user=self.user2
        )
        self.like2 = Like.objects.create(
            post=self.post2,
            user=self.user1
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_create_like(self):
        data = {
            'post': self.post2.pk
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user'], self.user1.id)
        self.assertEqual(Like.objects.count(), 1)

    def test_like_your_own_post_failed(self):
        data = {
            'post': self.post1.pk
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Like.objects.count(), 0)

    def test_delete_like_success(self):
        self.like1 = Like.objects.create(
            post=self.post1,
            user=self.user2
        )
        self.like2 = Like.objects.create(
            post=self.post2,
            user=self.user1
        )

        self.url = reverse('api:entities:like-detail', kwargs={'pk': self.like2.pk})
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, None)
        self.assertEqual(Like.objects.count(), 1)

    def test_delete_like_failed(self):
        self.like1 = Like.objects.create(
            post=self.post1,
            user=self.user2
        )
        self.like2 = Like.objects.create(
            post=self.post2,
            user=self.user1
        )

        self.url = reverse('api:entities:like-detail', kwargs={'pk': self.like1.pk})
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Like.objects.count(), 2)
