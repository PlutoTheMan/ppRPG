from django import forms
from .models import Character
from guilds.models import Guild

class NewCharacterForm(forms.ModelForm):
    """Representing New Character Form"""
    class Meta:
        model = Character
        fields = ["name"]

class FormGuildCreate(forms.ModelForm):
    """Representing new Guild Form"""
    class Meta:
        model = Guild
        fields = ["name"]