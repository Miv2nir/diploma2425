from django.db import models

import uuid

from django.contrib.auth.models import User
import json

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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    icon=models.ImageField(null=True,blank=True,upload_to='project_icons/')
    name=models.CharField(max_length=100)
    description=models.TextField(null=True,blank=True)
    tags=models.ManyToManyField(ProjectTag,blank=True)
    ACCESS_LEVEL = (
        ('A','Public'),
        ('B','Unlisted'),
        ('C','Private'),
    )
    access=models.CharField(max_length=1,choices=ACCESS_LEVEL,default='C')
    last_edited=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        self.name=self.name.replace('/','').replace('?','')
        super(Project,self).save(*args,**kwargs)

class DataFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file=models.FileField(upload_to='data_store/')
    EXTENSIONS= {
        'CSV':'.csv',
    }
    filetype=models.CharField(max_length=4,choices=EXTENSIONS)
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=100)
    description=models.TextField(null=True,blank=True)
    last_edited=models.DateTimeField(auto_now=True)
    display_in_guest_mode=models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        self.name=self.name.replace('/','').replace('?','')
        super(DataFile,self).save(*args,**kwargs)

class ProjectPin(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    
#cache models
#class LoaderParams(models.Model):
#    project=models.ForeignKey(Project,on_delete=models.CASCADE)
#    data_obj=models.ForeignKey(DataFile,on_delete=models.CASCADE)
#    order=models.IntegerField(default=0)


class FunctionParams(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    order=models.IntegerField(default=0)
    func_name=models.CharField(max_length=100)
    info=models.JSONField()
    
class FunctionStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    func=models.OneToOneField(FunctionParams,on_delete=models.CASCADE)
    info=models.JSONField(blank=True,default=dict)
    STATUSES=(
        ('NE','Not Executed'),
        ('EX','Executing'),
        ('OK','Done'),
        ('ER','Errored!')
    )
    status=models.CharField(choices=STATUSES,default='NE')

class RuntimeRenderResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    func_params=models.ForeignKey(FunctionParams,on_delete=models.CASCADE)
    result=models.TextField(blank=True)
    #file=models.FileField(upload_to='temp/',blank=True,null=True)

    
    
    

