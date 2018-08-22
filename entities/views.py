# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet

from .models import Post, Like
from .serializers import PostSerializer, LikeSerializer


class PostView(ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class LikeView(ModelViewSet):

    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user == obj.user:
            return super(LikeSerializer, self).destroy(request, *args, **kwargs)
        else:
            raise serializers.ValidationError('Not your like')
