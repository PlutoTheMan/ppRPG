from django.db import models
from django.contrib.auth.models import User

class LatestNews(models.Model):
    """Representing patch note's."""
    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=30)
    text = models.TextField()
    visible = models.BooleanField(choices=BOOL_CHOICES, default=True)
    image = models.ImageField(upload_to="latest_news/static/img", null=True, blank=True,)