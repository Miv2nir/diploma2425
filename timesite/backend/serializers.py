from rest_framework import serializers
import backend.models as models
import uuid
from django.contrib.auth.models import User

class ProjectSerializer(serializers.ModelSerializer):
    '''
    id = serializers.UUIDField(read_only=True)
    author = serializers.CharField(allow_blank=True)
    name=serializers.CharField(max_length=100)
    description=serializers.CharField(required=False)
    access=serializers.CharField(max_length=1)
    '''
    #this one is only for browsing the data
    class Meta:
        model=models.Project
        fields=['id','user','name','description','access']
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['pk','username']

class UserExtendedSerializer(serializers.Serializer):
    pk=serializers.IntegerField(read_only=True)
    username=serializers.CharField(allow_blank=True)
    display_name=serializers.CharField(allow_blank=True)
    has_pfp=serializers.BooleanField()
