# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import UserSerializer


class UserView(ModelViewSet):
    '''
    url: api/account/user/
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
