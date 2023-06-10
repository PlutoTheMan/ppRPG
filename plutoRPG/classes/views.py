from django.shortcuts import render

# Create your views here.
def classes(request):
    """
    Rendering classes page.
    :param request: Django request object.
    :return: (HttpResponse) classes page.
    """

    # Passing ctx just for pytest
    return render(request, "classes.html", {'content': 'classes'})