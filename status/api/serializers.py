from rest_framework import fields, serializers

from status.models import Status

class StatusSerializers(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = [
            'id',
            'user',
            'content',
            'image',
        ]
        read_only_fields = ['user']
        
    # def validate_content(self, value):
    #     if len(value) > 1000000:
    #         raise serializers.ValidationError('Content must be less than 1000000 characters.')
        
    #     return value
    
    def validate(self, data):
        content = data.get('content', None)
        if content == '':
            content = None
        image = data.get('image', None)
        if content == None and image == None :
            raise(serializers.ValidationError('Content or image is required.'))
        
        return data
