from django.shortcuts import render

# Create your views here.
def patch_notes(request):
    """
    Rendering patch notes page.
    :param request: Django request object.
    :return: (HttpResponse) patch notes page.
    """

    return render(request, "patch_notes.html", {'content': 'patch_notes'})