# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django_filters import rest_framework as filters

from account.models import User
from .models import Post


class PostFilter(filters.FilterSet):
    user = filters.ModelMultipleChoiceFilter(queryset=User.objects.all())

    class Meta:
        models = Post
        fields = ('user',)
