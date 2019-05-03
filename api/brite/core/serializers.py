from django.contrib.auth.models import User, Group
from rest_framework import serializers

from . import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'groups', 'password', 'url', 'username')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'url')


class RiskTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.RiskType
        fields = ('description', 'name', 'url', 'user')


class FieldTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.FieldType
        fields = ('kind', 'name', 'options', 'required', 'risk_type', 'url')


class RiskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Risk
        fields = ('client', 'risk_type', 'url')


class FieldSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Field
        fields = ('field_type', 'risk', 'value', 'url')
