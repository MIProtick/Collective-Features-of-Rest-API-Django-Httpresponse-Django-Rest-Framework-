from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from accounts.api.permissions import AnonymousPermission

from .serializers import UserRegistrationSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

User = get_user_model()


class AuthApiView(APIView):
    authentication_classes = []
    permission_classes = [AnonymousPermission]

    def post(self, request, *args, **kwargs):
        # print(request.user.is_anonymous)
        if request.user.is_authenticated:
            return Response({'details': 'You are already authenticated.'}, status=400)

        data = request.data
        if len(data) == 0:
            return Response({'details': 'No data provided.'}, status=401)

        username = data.get('username')
        password = data.get('password')
        # user = authenticate(username=username, password=password)
        qs = User.objects.filter(
            Q(username__iexact=username) |
            Q(email__iexact=username)
        ).distinct()
        if qs.count() == 1:
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(
                    token=token, user=user, request=request)
                return Response({'auth': response})

        return Response({'details': 'Invalid credentials'}, status=401)


class RegisterApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AnonymousPermission]
    
    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context(*args, **kwargs)
        context["request"] = self.request
        print(context)
        return context
    


# class RegisterApiView(APIView):
#     authentication_classes = []
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return Response({'details': 'You are already registered and authenticated.'}, status=400)

#         data = request.data
#         if len(data) == 0:
#             return Response({'details': 'No data provided.'}, status=401)

#         username = data.get('username',None)
#         password = data.get('password', None)
#         password2 = data.get('password2', None)
#         email = data.get('email', '')
        
#         if username is None or password is None or password2 is None:
#             return Response({'details': 'Invalid credentials.'}, status=401)

#         if password != password2:
#             return Response({'details': 'Passwords does not match'}, status=401)

#         qs = User.objects.filter(
#             Q(username__iexact=username) |
#             Q(email__iexact=username)
#         ).distinct()

#         if qs.exists():
#             return Response({'details': 'This user already exists.'}, status=401)
#         else:
#             user = User.objects.create(username=username, email=email)
#             user.set_password(password)
#             user.save()
#             payload = jwt_payload_handler(user)
#             token = jwt_encode_handler(payload)
#             response = jwt_response_payload_handler(
#                 token=token, user=user, request=request)
#             return Response({'reg': response}, status=201)

        
