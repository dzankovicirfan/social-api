# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import UserSerializer


class UserView(ModelViewSet):
    '''
    url: api/account/user/
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserSignUpView(CreateAPIView):
    '''
    Sign up view
    url: api/account/signup/
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED
        )
