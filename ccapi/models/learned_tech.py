"""Module creates Django Model for learned_tech"""
from django.db import models
from .user import User
from .tech import Tech

class LearnedTech(models.Model):
    """Create Class for LearnedTech Model"""
    uid = models.ForeignKey(User, on_delete= models.RESTRICT)
    tech = models.ForeignKey(Tech, on_delete= models.RESTRICT)
    last_updated = models.DateTimeField(auto_now=True)
