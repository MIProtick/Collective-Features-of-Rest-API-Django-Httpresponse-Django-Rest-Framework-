from django.urls import path, re_path

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from .views import ControlledUserDetailView, UserDetailView, UserStatusListView

urlpatterns = [
    # re_path(r"^user/(?P<id>\d+)/$", UserDetailView.as_view()),
    re_path(r"^user/(?P<id>\d+)/$", ControlledUserDetailView.as_view()),
    re_path(r"^user/(?P<username>\w+)/status/$", UserStatusListView.as_view()),
]
