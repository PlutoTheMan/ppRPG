from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Note(models.Model):
    """Representing Note model"""
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=9999)
