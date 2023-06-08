from django.db import models
from characters.models import Character

# Create your models here.
class Guild(models.Model):
    leader = models.OneToOneField(Character, on_delete=models.PROTECT)
    name = models.CharField(unique=True, max_length=40)
    members = models.ManyToManyField(Character, related_name='guild_members')
    date_created = models.DateTimeField(auto_now_add=True)
    pending_invites = models.ManyToManyField(Character, related_name='guild_invites')