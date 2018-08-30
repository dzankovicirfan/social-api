# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Post, Like


class PostAdmin(admin.ModelAdmin):
    list_display = list_display_links = ['title', 'user', 'likes_no']


class LikeAdmin(admin.ModelAdmin):
    list_display = list_display_links = ['post', 'user']


admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
