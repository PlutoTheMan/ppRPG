from django.shortcuts import render, redirect
from django.http import HttpResponse


# Create your views here.
def index(request):
    """
    Rendering homepage

    :param request: Django request object.
    :return: (HttpResponse) rendering homepage.
    """
    ctx = {'content': 'homepage'}
    if request.user:
        ctx['user'] = request.user
    return render(request, "index.html", ctx)
def display_credits(request):
    """
    Rendering credits page

    :param request: Django request object.
    :return: (HttpResponse) rendering credits page.
    """

    ctx = {'content': 'credits'}
    return render(request, "credits.html", ctx)
def download_credits_outfit(request):
    """
    Let user download CREDITS.csv file.

    :param request: Django request object.
    :return: (HttpResponse) Redirect to homepage or file content.
    """

    file_location = 'homepage/static/CREDITS.csv'
    try:
        with open(file_location, 'r') as f:
            file_data = f.read()

        # sending response
        response = HttpResponse(file_data, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="CREDITS.csv"'

    except IOError:
        return redirect("homepage")

    return response