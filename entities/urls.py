# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import path, include

from rest_framework import routers

from .views import PostView, LikeView


router = routers.SimpleRouter()
router.register(r'post', PostView)
router.register(r'like', LikeView)

app_name = 'entities'
urlpatterns = [
    path(r'', include(router.urls)),
]
