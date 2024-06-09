"""
URL configuration for socialNetwork project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from api import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/',views.UserRegisterView.as_view(),name='register'),
    path('api/login/', views.UserLoginView.as_view(), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/search/', views.UserSearchView.as_view(), name='user_search'),
    path('api/send-request/', views.sendFriendRequest, name='send_friend_request'),
    path('api/respond-request/<int:pk>/<str:action>/', views.respondToFriendRequest, name='respond_friend_request'),
    path('api/list-friends/', views.listFriends, name='list_friends'),
    path('api/list-pending-requests/', views.list_pending_requests, name='list_pending_requests'),
]
