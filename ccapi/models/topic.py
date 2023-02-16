"""Module creates Django Model for Topic"""
import uuid
from django.db import models
from .user import User
from .learned_tech import LearnedTech
from .goal import Goal

class Topic(models.Model):
    """Create Class for Topic Model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=150)
    uid = models.ForeignKey(User, on_delete= models.CASCADE)
    learned_tech = models.ForeignKey(LearnedTech, on_delete= models.CASCADE)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
