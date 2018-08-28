# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from socialapi import settings

from .models import User
import punter


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'date_joined', 'email',
            'password', 'is_active', 'additional_info'
        )
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'date_joined': {'read_only': True},
        }

    # def validate_email(self, value):
    #     response = punter.search(settings.hunter_key, value)
    #     # if response['status'] == 'success' and response['exist']:
    #     if response['status'] == 'success':
    #         return value
    #     else:
    #         raise serializers.ValidationError('Email does not exist')

    def create(self, validated_data):
        email = validated_data['email']

        # person = settings.clearbit.Enrichment.find(email=email, stream=True)

        # if person is not None:
        #     validated_data['additional_info'] = person

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
