from django.shortcuts import render
from django.views import View
from django.shortcuts import reverse, redirect
from .forms import *
from .models import PatchNote

def patch_notes(request):
    """
    Rendering patch notes page.
    :param request: Django request object.
    :return: (HttpResponse) patch notes page.
    """
    ctx = {
        'content': 'patch_notes',
        'patch_notes': PatchNote.objects.all().order_by('-date_created')[:10]
    }
    return render(request, "patch_notes.html", ctx)

class AdminPatchNotesManager(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            notes = PatchNote.objects.all()
            form = NewPatchNoteForm()
            ctx = {
                'form': form,
                'patch_notes': notes,
            }
            return render(request, 'admin_patch_notes.html', ctx)
        else:
            return redirect(reverse('homepage'))

    def post(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            form = NewPatchNoteForm(request.POST, request.FILES)
            notes = PatchNote.objects.all()
            if form.is_valid():
                patch_note = form.save(commit=False)
                patch_note.author = request.user
                patch_note.save()

                ctx = {
                    'patch_notes': notes,
                    'form': form,
                    'msg_success': 'Patch note saved successfully!'
                }
                return render(request, 'admin_patch_notes.html', ctx)
            else:
                ctx = {
                    'patch_notes': notes,
                    'form': form,
                    'msg_failed': 'Form has invalid data. Try again.'
                }
                return render(request, 'admin_patch_notes.html', ctx)
        else:
            return redirect(reverse('homepage'))

class AdminPatchNoteManager(View):
    def get(self, request, _id):
        if request.user.is_authenticated and request.user.is_superuser:
            note = PatchNote.objects.filter(pk=_id).first()
            form = NewPatchNoteForm({
                'title': note.title,
                'text': note.text,
                # 'visible': note.visible,
            })
            ctx = {
                'form': form,
                'patch_note': note,
            }
            return render(request, 'admin_patch_notes_edit.html', ctx)
        else:
            return redirect(reverse('homepage'))

    def post(self, request, _id=None):
        if request.user.is_authenticated and request.user.is_superuser:

            note = PatchNote.objects.filter(pk=_id).first()
            form = NewPatchNoteForm({
                'title': note.title,
                'text': note.text,
                'image': note.image,
            }, request.FILES)

            edit = request.POST.get('edit', False)
            delete = request.POST.get('delete', False)
            if edit:
                form = NewPatchNoteForm(request.POST, request.FILES)
                if form.is_valid():
                    form_patch_note = form.save(commit=False)
                    # Should change the author?
                    note.author = request.user
                    note.title = form_patch_note.title
                    note.text = form_patch_note.text
                    if form_patch_note.image:
                        note.image = form_patch_note.image
                    note.save()
            elif delete:
                note.delete()
                return redirect(reverse('admin_patch_notes'))

            ctx = {
                'form': form,
                'patch_note': note,
            }
            return render(request, 'admin_patch_notes_edit.html', ctx)
        else:
            return redirect(reverse('homepage'))