from rest_framework import serializers
import backend.models as models
import uuid

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
    