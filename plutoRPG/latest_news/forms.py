from django import forms
from latest_news.models import LatestNews

class NewLatestNewsForm(forms.ModelForm):
    """Representing New Latest News Form"""

    class Meta:
        model = LatestNews
        fields = ('title', 'text', 'image')