from django.urls import path, re_path

from .views import UpdateModelDetailView, UpdateModelListView

urlpatterns = [
    path('', UpdateModelListView.as_view(), name='updatemodellist'),
    re_path(r'^(?P<id>\d+)/$', UpdateModelDetailView.as_view(), name='updatemodeldetails'),
]
