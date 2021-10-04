from django.urls import path, re_path

from .views import StatusListView, StatusDetailsView #, StatusCreateView, StatusUpdateView, StatusDeleteView, StatusListView

urlpatterns = [
    path('', StatusListView.as_view(), name='statuslist'),
    re_path(r'^(?P<id>\d+)/$', StatusDetailsView.as_view(), name='statusdetails'),
    # re_path(r'create/$', StatusCreateView.as_view(), name='statusdetails'),
    # re_path(r'^(?P<id>\d+)/update/$', StatusUpdateView.as_view(), name='statusdetails'),
    # re_path(r'^(?P<id>\d+)/delete/$', StatusDeleteView.as_view(), name='statusdetails'),
]