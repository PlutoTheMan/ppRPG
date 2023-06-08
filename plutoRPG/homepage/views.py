from django.shortcuts import render, redirect
from django.http import HttpResponse


# Create your views here.
def index(request):
    ctx = {}
    if request.user:
        ctx['user'] = request.user
    return render(request, "index.html", ctx)

def display_credits(request):
    return render(request, "credits.html")

def download_credits_outfit(request):
    print("YES")
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