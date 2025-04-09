from django.db import models

import uuid

from django.contrib.auth.models import User

# Create your models here.
class UserInfo(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    display_name=models.TextField(blank=True,null=True)
    
    def __str__(self):
        return str(self.user)+"'s additional info"

class UserPFP(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    pfp=models.ImageField(null=True,blank=True,upload_to='user_pfps/')

class ProjectTag(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=100)
    
  
class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid5, editable=False)
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    icon=models.ImageField(null=True,blank=True,upload_to='project_icons/')
    name=models.CharField(max_length=100)
    description=models.TextField(null=True,blank=True)
    tags=models.ManyToManyField(ProjectTag,blank=True)