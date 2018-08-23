# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField


class User(AbstractUser):

    email = models.EmailField('Email address', blank=False, null=False)
    additional_info = JSONField(blank=True, null=True)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
