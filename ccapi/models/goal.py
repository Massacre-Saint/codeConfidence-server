"""Module creates Django Model for Goal"""
import uuid
from django.db import models
from .user import User
from .tech import Tech
from .learned_tech import LearnedTech

class Goal(models.Model):
    """Create Class for Goal Model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=25)
    learned_tech = models.ForeignKey(LearnedTech, on_delete= models.PROTECT)
    uid = models.ForeignKey(User, on_delete= models.RESTRICT)
    last_updated = models.DateTimeField(auto_now=True)
    progress = models.IntegerField(null=True)
