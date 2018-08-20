# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import path, include

from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

from .views import UserView

router = routers.SimpleRouter()
router.register(r'user', UserView)

app_name = 'account'
urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_jwt_token, name='login'),
    path('verify-jwf-token/', verify_jwt_token, name='verify_jwt_token'),
]
