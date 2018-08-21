# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from .models import Post, Like


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'text', 'user', 'likes_NO',
            'created_at', 'updated_at'
        )
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'user': {'read_only': True}
        }

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user

        return super(PostSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data['user'] = self.context['request'].user

        return super(PostSerializer, self).create(validated_data)


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('id', 'post', 'user')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user

        return super(PostSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data['user'] = self.context['request'].user

        return super(PostSerializer, self).create(validated_data)

    # def destroy(self, request, *args, **kwargs):
    #     if request.user == self.user:
    #         return super(LikeSerializer, self).destroy(request, *args, **kwargs)
    #     else:
    #         raise serializers.ValidationError('Not your like')
