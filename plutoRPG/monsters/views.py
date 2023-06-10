from django.shortcuts import render

# Create your views here.
def monsters(request):
    """
    Rendering monsters page.
    :param request: Django request object.
    :return: (HttpResponse) monsters page.
    """
    # Passing ctx just for pytest
    return render(request, "monsters.html", {'content': 'monsters'})
