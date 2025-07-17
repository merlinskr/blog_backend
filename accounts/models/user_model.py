from django.db import models
from .base_model import TimeStampedModel, SoftDeletableModel
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)  
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)  
        extra_fields.setdefault("is_superuser", True)
        
        return self.create_user(username, email, password, **extra_fields) 


class User(TimeStampedModel, SoftDeletableModel):
    username = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255,unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  
    is_superuser = models.BooleanField(default=False)  
    
    objects = CustomUserManager() 
    
    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['username'] 
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
        
    class Meta:
        ordering = ["-created_at"]