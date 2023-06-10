from django.shortcuts import render

# Create your views here.
def equipment(request):
    """
    Rendering equipment page.
    :param request: Django request object.
    :return: (HttpResponse) equipment page.
    """
    # Passing ctx just for pytest
    return render(request, "equipment.html", {'content': 'equipment'})