from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from rest_framework import exceptions
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.api.permissions import IsOwner, IsOwnerOrSuperuser

from accounts.api.user_management.serializers import UserDetailSerializer
from status.api.serializers import StatusNestedSerializers
from status.models import Status


User = get_user_model()


class UserDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = []
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'id'
    
    
class UserStatusListView(ListAPIView):
    serializer_class=StatusNestedSerializers
    
    def get_queryset(self, *args, **kwargs):
        username = self.kwargs.get('username', None)
        if username is None:
            return Status.objects.none()
        return Status.objects.filter(user__username=username)

        

class ControlledUserDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrSuperuser]
    # authentication_classes = []
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'id'
    
    
    # def check_object_permissions(self, request, obj):
    #     if request.user.id != int(self.request.parser_context['kwargs'].get('id')):
    #         raise exceptions.PermissionDenied(detail='You do not have permission.')
                
    #     return super().check_object_permissions(request, obj)
    
    
    def get_object(self, *args, **kwargs):
        get_id = self.request.GET.get('id', None)
        qs = self.queryset
        obj = None
        if get_id is not None:
            obj = get_object_or_404(qs, id=get_id)
            self.check_object_permissions(request=self.request, obj=obj)

        return super().get_object()
    
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
        # if(request.user.id == int(kwargs.get('id'))):
        #     print(request.user.id, int(kwargs.get('id')))
        #     return self.retrieve(request, *args, **kwargs)
        
        # return Response({'detail': 'You are not authenticated.'})


    

