from django.shortcuts import render

# Create your views here.
def worldmap(request):
    """
    Rendering worldmap page.
    :param request: Django request object.
    :return: (HttpResponse) worldmap page.
    """
    return render(request, "worldmap.html", {'content': 'worldmap'})