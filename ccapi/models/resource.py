"""Module creates Django Model for Resource"""
from django.db import models
from .tech import Tech
from .bookmark import Bookmark

class Resource(models.Model):
    """Creates class for Resource Model"""
    id = models.IntegerField(primary_key=True)
    bookmark = models.ForeignKey(Bookmark, on_delete= models.PROTECT)
    assigned_to = models.CharField(max_length=100)
    tech = models.ForeignKey(Tech, on_delete= models.PROTECT)
