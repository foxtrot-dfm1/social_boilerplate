from django.urls import path

from .views import *

urlpatterns = [
    path('', UserRetrieveView.as_view()),
    path('login/', LoginUserView.as_view()),
    path('signup/', RegisterUserView.as_view()),
]