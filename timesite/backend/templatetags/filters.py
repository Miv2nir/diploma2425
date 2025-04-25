from django import template
from django.template.defaulttags import register
import backend.forms as forms
import backend.models as models
from django.contrib.auth.models import User
from backend import functions

from django.conf import settings

register=template.Library()

@register.filter #django template filter TODO: move it out elsewhere
def get_item(dictionary,key):
    return dictionary.get(key)

@register.filter
def get_display_name(user):
    try:
        return models.UserInfo.objects.filter(user=user)[0].display_name
    except IndexError: #fallback
        return user.username

@register.filter #get user pfp
def get_pfp(user):
    try:
        pfp_obj=models.UserPFP.objects.filter(user=user)[0]
        #return settings.MEDIA_ROOT+pfp_obj.pfp
        return pfp_obj.pfp.url
    except IndexError:
        return settings.STATIC_URL+'pfp_placeholder.png'
    except ValueError:
        return settings.STATIC_URL+'pfp_placeholder.png'
    
@register.filter #get user pfp
def get_icon(item:models.Project):
    if item.icon:
        return item.icon.url
    else:
        return settings.STATIC_URL+'icon_placeholder.png'

@register.filter #get the last 5 recent projects
def get_projects(user):
    return functions.get_last_projects(user,5)

@register.filter
def get_project_visibility(proj_obj:models.Project):
    if proj_obj.access=='A':
        return ''
    elif proj_obj.access=='B':
        return '(Unlisted)'
    else:
        return '(Private)'