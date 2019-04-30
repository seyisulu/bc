from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('auth', views.Auth.as_view(), name='auth'),
    path('groups', views.GroupList.as_view(), name='group-list'),
    path('users', views.UserAdd.as_view(), name='user-add'),
    path('users/<int:pk>', views.UserInfo.as_view(), name='user-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
