from django.shortcuts import render

# Create your views here.
def patch_notes(request):
    return render(request, "patch_notes.html")