from django.urls import path

from ..views import *

urlpatterns = [
    path("tags/", GetTagListView.as_view(), name="tag-list"),
    path("tags/create/", CreateTagView.as_view(), name="tag-create"),
    path("tags/<int:pk>/", GetTagView.as_view(), name="tag-detail"),
    path("tags/<int:pk>/update/", UpdateTagView.as_view(), name="tag-update"),
    path("tags/<int:pk>/delete/", DeleteTagView.as_view(), name="tag-delete"),
]
