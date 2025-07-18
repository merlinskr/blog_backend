from django.urls import path

from accounts.views.user_view import GetUserListView, GetUserView
from ..views import CreateUserView,DeleteUserView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path('create/',CreateUserView.as_view(),name='create_user'),
    path('delete/<int:pk>/',DeleteUserView.as_view(),name='delete_user'),
    path('list/', GetUserListView.as_view(), name='list_users'),
    path('detail/<int:pk>/', GetUserView.as_view(), name='user_detail'),
]