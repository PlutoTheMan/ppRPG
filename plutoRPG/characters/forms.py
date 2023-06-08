from django import forms
from .models import Character
from guilds.models import Guild

class NewCharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ["name"]

class FormGuildCreate(forms.ModelForm):
    class Meta:
        model = Guild
        fields = ["name"]