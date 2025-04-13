from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

import backend.models as models
import backend.serializers as serializers

#@csrf_exempt #TODO: remove this after csrf validation is complete
def get_project(request,id):
    '''
    test api to retrieve project metadata info
    '''
    try:
        project = models.Project.objects.get(pk=id)
    except models.Project.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method=='GET':
        serializer=serializers.ProjectSerializer(project)
        return JsonResponse(serializer.data)