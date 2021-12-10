from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from status.api.serializers import StatusNestedSerializers


User = get_user_model()

class UserDetailSerializer(serializers.ModelSerializer):
    status_list = serializers.SerializerMethodField(read_only=True)
    owner = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ['user_permissions', 'groups', 'date_joined', 'password']
        read_only_fields = ['status_list', 'is_staff', 'last_login', 'is_active', 'is_superuser', 'owner']
    
    def get_status_list(self, obj):
        statuss = obj.status_set.all()
        lists = StatusNestedSerializers(statuss, many=True).data
        return lists
        
    def get_owner(self, obj):
        return obj.id
        
