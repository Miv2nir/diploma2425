from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, JsonResponse
import backend.forms as forms
import backend.models as models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def find_projects_by_name(prompt=''):
    if not prompt:
        lookup=models.Project.objects.filter(access='A')
    else:
        lookup=models.Project.objects.filter(access='A',name__icontains=prompt)
    return lookup