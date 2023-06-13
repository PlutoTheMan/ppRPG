from django import forms
from patch_notes.models import PatchNote

class NewPatchNoteForm(forms.ModelForm):
    """Representing New Patch Note Form"""

    class Meta:
        model = PatchNote
        fields = ('title', 'text', 'image')