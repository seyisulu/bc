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


class FieldTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        extra_kwargs = {'options': {'allow_null': True}}
        fields = ('kind', 'name', 'options', 'required', 'risk_type', 'url')
        model = FieldType


class RiskTypeSerializer(serializers.HyperlinkedModelSerializer):
    created = serializers.DateTimeField(
        default=serializers.CreateOnlyDefault(timezone.now), read_only=True)
    field_types = FieldTypeSerializer(many=True, read_only=False)
    updated = serializers.DateTimeField(default=timezone.now, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        extra_kwargs = {'url': {'view_name': 'risk_type'}}
        fields = (
            'created',
            'description',
            'field_types',
            'name',
            'updated',
            'url',
            'user'
        )
        model = RiskType

    def create(self, validated_data):
        print('Creating risk type...')
        field_types_data = validated_data.pop('field_types')
        print('Popped field types...')
        risk_type = RiskType(**validated_data)
        print('Instantiating risk type...')
        risk_type.save()
        print('Created risk type...')
        FieldType.objects.bulk_create([
            FieldType(risk_type=risk_type, **f) for f in field_types_data
        ])
        print('Added field types...')
        return RiskType.objects.get(pk=risk_type.pk)


class FieldSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Field
        fields = ('field_type', 'risk', 'value', 'url')


class RiskSerializer(serializers.HyperlinkedModelSerializer):
    created = serializers.DateTimeField(
        default=serializers.CreateOnlyDefault(timezone.now), read_only=True)
    fields = FieldSerializer(many=True, read_only=False)
    risk_type = RiskTypeSerializer()
    updated = serializers.DateTimeField(default=timezone.now, read_only=True)

    class Meta:
        model = Risk
        fields = ('client', 'created', 'fields', 'risk_type', 'updated', 'url')

    def create(self, validated_data):
        risk_type = RiskType.objects.get(pk=validated_data.pop('risk_type'))
        fields_data = validated_data.pop('fields')
        risk = Risk(risk_type=risk_type, **validated_data)
        risk.save()
        Field.objects.bulk_create([
            Field(risk=risk, **f) for f in fields_data
        ])
        return Risk.objects.get(pk=risk.pk)
