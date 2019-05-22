from django.db import models
from django.contrib.auth.models import User #import base/default user model
# Create your models here.

class UserProfileInfo(models.Model):
    #creating a model class to add in additional info that the default user does not have
    user = models.OneToOneField(User,on_delete=models.CASCADE) #onetoone extends the class, do not inherit from User(database will think multi instances of same user)

    #additional classes
    portfolio_site = models.URLField(blank=True) #blan=True means not required to be filled in
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True) #upload_to id location to store images, subfolder of media

    def __str__(self):
        return self.user.username  #username is a default attribute of User
