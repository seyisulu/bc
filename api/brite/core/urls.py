from django.urls import path

from . import views

urlpatterns = [
    path('auth', views.Auth.as_view(), name='auth'),
    path('groups', views.GroupList.as_view(), name='groups'),
    path('risk_types', views.RiskTypeList.as_view(), name='risk_types'),
    path('risk_types/<int:pk>', views.RiskTypeInfo.as_view(), name='risk_type'),
    path('users', views.UserAdd.as_view(), name='users'),
    path('users/<int:pk>', views.UserInfo.as_view(), name='user'),
]
