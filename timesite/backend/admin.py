from django.contrib import admin

from backend.models import *

# Register your models here.

admin.site.register(UserInfo)
admin.site.register(UserPFP)

admin.site.register(Project)
admin.site.register(ProjectTag)

#debug
admin.site.register(DataFile)
admin.site.register(ProjectPin)
admin.site.register(FunctionParams)
