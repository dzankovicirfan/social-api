# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins, viewsets

from .models import Post, Like
from .serializers import PostSerializer, LikeSerializer


class PostView(ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user == obj.user:
            return super(PostView, self).destroy(request, *args, **kwargs)
        else:
            raise serializers.ValidationError('Not your post')


class LikeView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):

    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user == obj.user:
            return super(LikeView, self).destroy(request, *args, **kwargs)
        else:
            raise serializers.ValidationError('Not your like')
