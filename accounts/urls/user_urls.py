from django.urls import path

from ..views import (
    CreateUserView,
    DeleteUserView,
    GetUserListView,
    GetUserView,
    UpdateUserView,
)
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("create/", CreateUserView.as_view(), name="create_user"),
    path("delete/<int:pk>/", DeleteUserView.as_view(), name="delete_user"),
    path("list/", GetUserListView.as_view(), name="list_users"),
    path("detail/<int:pk>/", GetUserView.as_view(), name="user_detail"),
    path("update/<int:pk>/", UpdateUserView.as_view(), name="update_user"),
]
