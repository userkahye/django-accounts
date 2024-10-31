from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):

    def get_by_natural_key(self, username):
        return self.get(username=username)

class Client(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    
    USERNAME_FIELD = 'username'  # or 'email', depending on how users log in
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()
 

