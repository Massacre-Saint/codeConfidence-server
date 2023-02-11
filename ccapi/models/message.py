"""Module creates Django Model for Message"""
from django.db import models

class Message(models.Model):
    """Create Class for Message Model"""
    title= models.CharField(max_length=500)
