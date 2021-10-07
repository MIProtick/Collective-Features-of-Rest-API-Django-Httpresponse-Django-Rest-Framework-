from datetime import timedelta
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.http import request
from django.utils import timezone
from rest_framework import fields
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
REFRESH_DELAY = api_settings.JWT_REFRESH_EXPIRATION_DELTA


User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    token_expires = serializers.SerializerMethodField(read_only=True)
    # token_response = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        # fields = '__all__'
        exclude = ['user_permissions', 'groups', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}}

    def validated_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError(
                'User already exists with this email.')
        return value

    def validated_username(self, value):
        qs = User.objects.filter(username__iexact=value)
        if qs.exists():
            raise serializers.ValidationError(
                'User already exists with this username.')
        return value

    def get_token(self, obj):
        user = obj
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def get_token_expires(self, obj):
        expires = timezone.now() + REFRESH_DELAY + timedelta(seconds=200),
        return expires

    # def get_token_response(self, obj):
    #     user = obj
    #     payload = jwt_payload_handler(user)
    #     token = jwt_encode_handler(payload)
    #     request = self.context['request']
    #     response = jwt_response_payload_handler(
    #         token=token, user=user, request=request)
    #     return response

    def validate(self, data):
        pw = data.get('password')
        pw2 = data.pop('password2')
        if pw != pw2:
            raise serializers.ValidationError('Password did not matched.')

        return data

    def create(self, validated_data):
        user_obj = User(
            username=validated_data.get('username'),
            email=validated_data.get('email')
        )
        user_obj.set_password(validated_data.get('password'))
        # user_obj.is_active = False
        user_obj.save()
        return user_obj
    
    # # for default validation
    # def create(self, validated_data):
    #     return super().create(validated_data)
