"""Module creates Django Model for Resource"""
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .learned_tech import LearnedTech
from .bookmark import Bookmark

class Resource(models.Model):
    """Creates class for Resource Model"""
    bookmark = models.ForeignKey(Bookmark, on_delete= models.CASCADE)
    assigned_to = models.ForeignKey(ContentType, on_delete= models.PROTECT, null=True)
    object_id = models.CharField(max_length=50, null=True)
    content_object = GenericForeignKey('assigned_to', 'object_id')
    tech = models.ForeignKey(LearnedTech, on_delete= models.PROTECT)
