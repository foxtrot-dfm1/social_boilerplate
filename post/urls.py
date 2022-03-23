from django.urls import path

from .views import *

app_name = "posts"

urlpatterns = [
    path("<int:id>", PostView.as_view()),
    path("<int:id>/like", PostLike.as_view()),
    path("<int:id>/unlike", PostUnlike.as_view()),
    path("create/", PostView.as_view()),
    path("list/", PostListView.as_view()),
]