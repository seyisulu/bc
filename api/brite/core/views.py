from django.contrib.auth.models import Group, User
from rest_framework import generics, permissions, response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .permissions import IsAdmin
from .serializers import UserSerializer, GroupSerializer


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
            'user_id': user.pk,
        })


class UserAdd(generics.CreateAPIView):
    """Creates new user."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class UserInfo(generics.RetrieveAPIView):
    """Retrieve, update or delete a user instance."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupList(generics.ListAPIView):
    """List all groups."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAdmin,)
