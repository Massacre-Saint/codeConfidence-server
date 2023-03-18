"""Module creates Django Model for BookMark"""
from django.db import models

class Bookmark(models.Model):
    """Create class for Bookmark Model"""
    id= models.IntegerField(primary_key=True)
    index = models.PositiveIntegerField()
    parent_id = models.PositiveIntegerField()
    title = models.CharField(max_length=150)
    url = models.CharField(max_length=100, null=True)
