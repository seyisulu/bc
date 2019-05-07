from django.contrib.auth.models import User, Group
from django.utils import timezone
from rest_framework import serializers

from .models import Field, FieldType, Risk, RiskType


class UserSerializer(serializers.HyperlinkedModelSerializer):
    pk = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('email', 'groups', 'password', 'pk', 'url', 'username')
        extra_kwargs = {
            'password': {'write_only': True},
            'url': {'view_name': 'user'},
        }

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'url')


class FieldTypeSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
            'options': {'allow_null': True},
            'pk': {'read_only': True},
            'risk_type': {'read_only': True},
        }
        fields = ('kind', 'name', 'options', 'pk', 'required', 'risk_type')
        model = FieldType


class RiskTypeSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(
        default=serializers.CreateOnlyDefault(timezone.now), read_only=True)
    field_types = FieldTypeSerializer(many=True, read_only=False)
    updated = serializers.DateTimeField(default=timezone.now, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        extra_kwargs = {
            'pk': {'read_only': True},
            'url': {'view_name': 'risk_type'},
        }
        fields = (
            'created',
            'description',
            'field_types',
            'name',
            'pk',
            'updated',
            'url',
            'user'
        )
        model = RiskType

    def create(self, validated_data):
        field_types_data = validated_data.pop('field_types')
        risk_type = RiskType(**validated_data)
        risk_type.save()
        FieldType.objects.bulk_create([
            FieldType(risk_type=risk_type, **f) for f in field_types_data
        ])
        return RiskType.objects.get(pk=risk_type.pk)


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
            'pk': {'read_only': True},
            'risk': {'read_only': True},
        }
        model = Field
        fields = ('field_type', 'pk', 'risk', 'value')


class RiskSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(
        default=serializers.CreateOnlyDefault(timezone.now), read_only=True)
    fields = FieldSerializer(many=True, read_only=False)
    updated = serializers.DateTimeField(default=timezone.now, read_only=True)

    class Meta:
        model = Risk
        fields = ('client', 'created', 'fields', 'pk', 'risk_type', 'updated')

    def create(self, validated_data):
        fields_data = validated_data.pop('fields')
        risk = Risk(**validated_data)
        risk.save()
        Field.objects.bulk_create([Field(risk=risk, **f) for f in fields_data])
        return Risk.objects.get(pk=risk.pk)
