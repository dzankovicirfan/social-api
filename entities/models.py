# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from account.models import User


class Post(models.Model):
    title = models.CharField('Title', max_length=100, blank=True, null=True)
    text = models.TextField()
    user = models.ForeignKey(
        User, related_name='posts', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.title

    @property
    def likes_no(self):
        return self.likes.all().count()

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'


class Like(models.Model):
    post = models.ForeignKey(
        Post, related_name='likes', on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, related_name='likes', on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("post", "user")
        verbose_name = 'like'
        verbose_name_plural = 'likes'
