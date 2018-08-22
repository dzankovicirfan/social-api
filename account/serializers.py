# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'date_joined', 'email',
            'password', 'is_active',
        )
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'date_joined': {'read_only': True},
        }

    def create(self, validated_data):

        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    def update(self, instance, validated_data):

        user = super(UserSerializer, self).update(instance, validated_data)

        if validated_data.get('password', None):
            user.set_password(validated_data['password'])
            user.save()
        return user
