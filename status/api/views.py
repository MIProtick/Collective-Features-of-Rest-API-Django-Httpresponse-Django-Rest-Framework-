import json
# from django.shortcuts import get_object_or_404
# from app.utils import is_valid_json
# from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView #, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.mixins import CreateModelMixin #, UpdateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
# from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from accounts.api.permissions import IsOwnerOrReadOnly
# from rest_framework.response import Response
# from status.api.utils import custom_response

from status.models import Status
from .serializers import StatusSerializers


class StatusDetailsView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # authentication_classes = []
    queryset = Status.objects.all()
    serializer_class = StatusSerializers
    lookup_field = 'id'
        
        
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    
    # def perform_destroy(self, instance):
    #     if instance is not None:
    #         return instance.delete()
    #     return None
    
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)




class StatusListView(CreateModelMixin, 
                    # RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, 
                    ListAPIView):
    permission_classes          = [IsAuthenticatedOrReadOnly]
    # authentication_classes    = [SessionAuthentication]
    queryset                    = Status.objects.all()
    serializer_class            = StatusSerializers
    search_fields               = ['user__username', 'user__email', 'content',]
    # lookup_field              = 'id'
    passed_id                   = None
    passed_data                 = None

    def is_valid_json(self, data):
        try:
            js_data = json.loads(data)
            return True
        except:
            return False
            
    # def check_get_id(self, request):
    #     url_get_id = request.GET.get('id', None)
    #     passed_body = request.data
    #     self.passed_data = passed_body
        
    #     if is_valid_json(passed_body):
    #         passed_body = json.loads(passed_body)
    #     body_get_id = passed_body.get('id', None)
        
    #     get_id = url_get_id or body_get_id or None
    #     self.passed_id = get_id
    #     return get_id
            

    def get_queryset(self):
        request = self.request
        qs = Status.objects.all()
        search = request.GET.get('q', None)
        if search is not None:
            qs = qs.filter(content__icontains=search)
        return qs

    # def get_object(self):
    #     request = self.request
    #     get_id = request.GET.get('id', None) or self.passed_id
    #     qs = self.get_queryset()
    #     obj = None
    #     if get_id is not None:
    #         obj = get_object_or_404(qs, id=get_id)
    #         self.check_object_permissions(request=request, obj=obj)

    #     return obj
        
        
    # def perform_destroy(self, instance):
    #     if instance is not None:
    #         return instance.delete()
    #     return None
    
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

   
    # def get(self, request, *args, **kwargs):
    #     get_id = self.check_get_id(request)
    #     if get_id is not None:
    #         return self.retrieve(request, *args, **kwargs)

    #     return super().get(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     get_id = self.check_get_id(request)
    #     if get_id is not None:
    #         return self.update(request, *args, **kwargs)
    #     else:
    #         return custom_response(json.dumps({'Details':"No 'id' provided."}), status=404)

    # def patch(self, request, *args, **kwargs):
    #     get_id = self.check_get_id(request)
    #     if get_id is not None:
    #         return self.partial_update(request, *args, **kwargs)
    #     else:
    #         return custom_response(json.dumps({'Details':"No 'id' provided."}), status=404)

    # def delete(self, request, *args, **kwargs):
    #     get_id = self.check_get_id(request)
    #     if get_id is not None:
    #         return self.destroy(request, *args, **kwargs)
    #     else:
    #         return custom_response(json.dumps({'Details':"No 'id' provided."}), status=404)







# class StatusListApiView(APIView):
#     permission_classes = []
#     authentication_classes = []

#     def fetchQuerySet(self):
#         qs = Status.objects.all()
#         return qs

#     def fetchData(self, id, *args, **kwargs):
#         qs = self.fetchQuerySet().filter(id=id)
#         if qs.count() == 1:
#             return qs.first()
#         else: return None

#     def get(self, request, format=None):
#         qs = self.fetchQuerySet()
#         serialized_data = StatusSerializers(qs, many=True)
#         return Response(serialized_data.data)


# class StatusListView(ListCreateAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializers

#     def get_queryset(self):
#         qs = Status.objects.all()
#         search = self.request.GET.get('search')
#         if search is not None:
#             qs = qs.filter(content__icontains = search)
#         return qs

#     # def perform_create(self, serializer):
#     #     serializer.save(user=self.request.user)


# # class StatusListView(CreateModelMixin, ListAPIView):
# #     permission_classes = []
# #     authentication_classes = []
# #     queryset = Status.objects.all()
# #     serializer_class = StatusSerializers

# #     def get_queryset(self):
# #         qs = Status.objects.all()
# #         search = self.request.GET.get('search')
# #         if search is not None:
# #             qs = qs.filter(content__icontains = search)
# #         return qs

# #     def post(self, request, *args, **kwargs):
# #         return self.create(request, *args, **kwargs)

# #     # def perform_create(self, serializer):
# #     #     serializer.save(user=self.request.user)


# # class StatusCreateView(CreateAPIView):
# #     permission_classes = []
# #     authentication_classes = []
# #     queryset = Status.objects.all()
# #     serializer_class = StatusSerializers

# #     def perform_create(self, serializer):
# #         serializer.save(user=self.request.user)


# class StatusDetailView(RetrieveUpdateDestroyAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializers
#     lookup_field = 'id'


# # class StatusDetailView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
# #     permission_classes = []
# #     authentication_classes = []
# #     queryset = Status.objects.all()
# #     serializer_class = StatusSerializers
# #     lookup_field = 'id'

# #     def put(self, request, *args, **kwargs):
# #         return self.update(request, *args, **kwargs)

# #     def delete(self, request, *args, **kwargs):
# #         return self.destroy(request, *args, **kwargs)


# class StatusUpdateView(UpdateAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializers
#     lookup_field = 'id'


# class StatusDeleteView(DestroyAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializers
#     lookup_field = 'id'
