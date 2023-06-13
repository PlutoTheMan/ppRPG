from django.shortcuts import render, redirect
from django.http import HttpResponse
from latest_news.models import LatestNews

# Create your views here.
def index(request):
    """
    Rendering homepage

    :param request: Django request object.
    :return: (HttpResponse) rendering homepage.
    """
    latest_news = LatestNews.objects.all().order_by('-date_created')[:10]

    ctx = {
        'content': 'homepage',
        'latest_news': latest_news,
        'superuser': False,
    }

    if request.user:
        ctx['user'] = request.user

    if request.user.is_superuser:
        ctx['superuser'] = True

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