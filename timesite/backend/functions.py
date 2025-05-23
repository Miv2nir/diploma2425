from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, JsonResponse
import backend.forms as forms
import backend.models as models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db.models import Q

def find_projects_by_name(prompt='',only_public=True,user=None):
    if only_public:
        if not prompt:
                lookup=models.Project.objects.filter(access='A')
        else:
                lookup=models.Project.objects.filter(access='A',name__icontains=prompt)
    elif user: #include objects where the user is the owner in the search
        if not prompt:
                lookup=models.Project.objects.filter(Q(access='A') | Q(user=user))
        else:
                lookup=models.Project.objects.filter(Q(access='A') | Q(user=user),name__icontains=prompt)
        #lookup = list(chain(lookup,lookup_second))
    return lookup

def verify_project_viewing_eligibility(proj_obj,user):
    #firstly, check if public or unlisted
    if proj_obj.access=='A' or proj_obj.access=='B':
        return True
    else: #access set to private
        if proj_obj.user==user:
            return True
        return False #not allowed

def get_last_projects(user,items=5):
    return models.Project.objects.filter(user=user).order_by('-last_edited')[:items]
    