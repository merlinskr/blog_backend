from django.urls import path
from ..views import CreateUserView,DeleteUserView

urlpatterns = [
    path('create/',CreateUserView.as_view(),name='create_user'),
    path('delete/<int:pk>/',DeleteUserView.as_view(),name='delete_user')
]