from django import template
from django.template.defaulttags import register
import backend.forms as forms
import backend.models as models
from django.contrib.auth.models import User

from django.conf import settings

register=template.Library()

@register.filter #django template filter TODO: move it out elsewhere
def get_item(dictionary,key):
    return dictionary.get(key)

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