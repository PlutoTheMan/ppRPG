from django import forms
from patch_notes.models import PatchNote

class NewPatchNoteForm(forms.ModelForm):
    """Representing New Character Form"""


    class Meta:
        model = PatchNote
        fields = ('title', 'text', 'image')
        # widgets = {
        #     'visible': forms.RadioSelect
        # }

    # def __init__(self, *args, **kwargs):
    #     super(NewPatchNoteForm, self).__init__(*args, **kwargs)
    #     self.fields['image'].required = False