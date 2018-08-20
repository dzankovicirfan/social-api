# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    email = models.EmailField('Email address', blank=False, null=False)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
