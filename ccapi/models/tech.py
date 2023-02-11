"""Module creates Django Model for Tech"""
from django.db import models

class Tech(models.Model):
    """Create Class for Tech Model"""
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    doc_url = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200)
