from django.shortcuts import render, redirect
from .forms import *
from django.views import View
from .models import Note

# Create your views here.
class NotesView(View):
    def get(self, request):
        if request.user.is_authenticated:
            o = Note.objects.filter(author=request.user).first()

            if o is not None:
                notes_form = NotesForm(initial={'content': o.content})
            else:
                notes_form = NotesForm()
            
            ctx = {'form': notes_form}
            return render(request, 'notes.html', ctx)
        else:
            return redirect('homepage')

    def post(self, request):
        if request.user.is_authenticated:
            notes_form = NotesForm(request.POST)
            if notes_form.is_valid():
                content = notes_form.cleaned_data['content']
                o = Note.objects.filter(author=request.user).first()
                if o is not None:
                    o.content = content
                    o.save()
                else:
                    Note.objects.create(author=request.user, content=content)
                ctx = {'form': notes_form}
                return render(request, 'notes.html', ctx)
        else:
            return redirect('homepage')