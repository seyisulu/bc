from django.contrib.auth.models import Group, User
from rest_framework import generics, permissions, response, status, views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .models import Risk, RiskType
from .permissions import IsAdmin, IsOwner
from .serializers import (UserSerializer, GroupSerializer,
                          RiskSerializer, RiskTypeSerializer)


class Auth(ObtainAuthToken):
    """Obtain authentication token."""
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return response.Response({
            'admin': user.is_staff,
            'email': user.email,
            'token': token.key,
            'pk': user.pk,
        })


class UserAdd(generics.CreateAPIView):
    """Creates new user."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class UserInfo(generics.RetrieveAPIView):
    """Retrieve a User instance."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupList(generics.ListAPIView):
    """List all groups."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAdmin,)


class RiskTypeList(generics.ListCreateAPIView):
    """List all risk types for logged in user."""
    def get_queryset(self):
        return RiskType.objects.filter(user=self.request.user)

    serializer_class = RiskTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class RiskTypeInfo(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a RiskType instance."""
    def get_queryset(self):
        return RiskType.objects.filter(user=self.request.user)

    serializer_class = RiskTypeSerializer
    permission_classes = (IsOwner,)


class RiskList(generics.ListCreateAPIView):
    """List all risks for logged in user."""
    def get_queryset(self):
        risk_types = RiskType.objects.values_list(
            'pk', flat=True).filter(user=self.request.user)
        return Risk.objects.filter(risk_type__in=risk_types)

    serializer_class = RiskSerializer
    permission_classes = (permissions.IsAuthenticated,)


class RiskInfo(generics.RetrieveAPIView):
    """Retrieve a Risk instance."""
    def get_queryset(self):
        risk_types = RiskType.objects.values_list(
            'pk', flat=True).filter(user=self.request.user)
        return Risk.objects.filter(risk_type__in=risk_types)

    serializer_class = RiskSerializer
    permission_classes = (permissions.IsAuthenticated,)
