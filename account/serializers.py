# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from .models import User
from pyhunter import PyHunter
import clearbit


hunter = PyHunter('c60c4406617d0f1ad2c24526e5fa258c96a5a878')
clearbit.key = 'sk_d4ff07e1dfde61281f450c0ae22936af'


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

    def create(self, validated_data):
        # komentarisano da ne bih pri testiranju trosio zahteve prema hunteru
        # ogranicen je na 100 zahteva mesecno

        email = validated_data['email']
        # email_exist = hunter.email_verifier(email)

        # if not email_exist:
        #     raise serializers.ValidationError('Email does not exist')

        person = clearbit.Enrichment.find(email=email, stream=True)

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
