from django import forms

class NotesForm(forms.Form):
    content = forms.CharField(label=False, widget=forms.Textarea(), max_length=999)