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

    def validate_email(self, value):
        if self.context['request'].GET.get('bot', False) == '1':
            return value
        response = punter.search(settings.HUNTER_KEY, value)
        if response['status'] == 'success' and response['exist']:
            return value
        else:
            raise serializers.ValidationError('Email does not exist on emailhunter')

    def create(self, validated_data):
        email = validated_data['email']
        validated_data['is_active'] = True
        person = None

        if self.context['request'].GET.get('bot', False) != '1':
            person = settings.clearbit.Enrichment.find(email=email, stream=True)

        if person is not None:
            validated_data['additional_info'] = person

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
