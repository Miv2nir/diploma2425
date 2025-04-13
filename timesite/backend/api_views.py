from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

import backend.models as models
import backend.serializers as serializers

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required

#TODO: rewrite login_required to dump a 401 if user not authorized
# the frontend will need to preserve the url and redirect to /login with query being the current logged in page

#@login_required
def get_project(request,id):
    '''
    test api to retrieve project metadata info
    '''
    #if not request.user.pk: #None if not logged in, returns a value otherwise
        
    #check if exists
    try:
        project = models.Project.objects.get(pk=id)
    except models.Project.DoesNotExist:
        return HttpResponse(status=404)
    if request.method=='GET':
        serializer=serializers.ProjectSerializer(project)
        return JsonResponse(serializer.data)