from django.urls import path

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from .views import AuthApiView, RegisterApiView

urlpatterns = [
    path("login/", AuthApiView.as_view()),
    path("register/", RegisterApiView.as_view()),
    path("token/", obtain_jwt_token),
    path("token/refresh/", refresh_jwt_token),
]
