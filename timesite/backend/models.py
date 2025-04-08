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