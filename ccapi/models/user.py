"""Module creates Django Model for User"""
from django.db import models

class User(models.Model):
    """Create Class for User Model"""
    display_name = models.CharField(max_length=25)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    bio = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200)
    created_on = models.DateField(auto_now_add=True)
    is_admin = models.BooleanField(default = False)
    email = models.CharField(max_length=50)
    uid = models.CharField(max_length=40)
