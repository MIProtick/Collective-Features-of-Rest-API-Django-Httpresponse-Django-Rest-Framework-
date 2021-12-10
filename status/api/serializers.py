from rest_framework import fields, serializers
from accounts.api.auth.serializers import UserDescriptionSerializer

from status.models import Status


class StatusNestedSerializers(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Status
        fields = [
            'id',
            'user',
            'content',
            'image',
            'image_url',
        ]
        read_only_fields = ['user']
    
    def get_image_url(self, obj):
        print(type(obj.image))
        if obj.image :
            return f'/{obj.image}'
        else:
            return f'/{obj.image}'


class StatusSerializers(serializers.ModelSerializer):
    user = UserDescriptionSerializer(read_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)
    uri = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Status
        fields = [
            'id',
            'user',
            'content',
            'image',
            'image_url',
            'uri',
        ]
        read_only_fields = ['user', 'uri']
        
    # def validate_content(self, value):
    #     if len(value) > 1000000:
    #         raise serializers.ValidationError('Content must be less than 1000000 characters.')
        
    #     return value
    
    def get_image_url(self, obj):
        return f'/{obj.image}'
        
    def get_uri(self, obj):
        return f'/api/status/{obj.id}'
    
    def validate(self, data):
        content = data.get('content', None)
        if content == '':
            content = None
        image = data.get('image', None)
        if content == None and image == None :
            raise(serializers.ValidationError('Content or image is required.'))
        
        return data
