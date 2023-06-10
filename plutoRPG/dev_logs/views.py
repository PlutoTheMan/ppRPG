from django.shortcuts import render

# Create your views here.
def dev_logs(request):
    """
    Rendering dev logs page. Content hardcoded in .html template.
    :param request: Django request object.
    :return: (HttpResponse) dev logs page.
    """
    # Passing ctx just for pytest
    return render(request, "dev_logs.html", {'content': 'devlogs'})