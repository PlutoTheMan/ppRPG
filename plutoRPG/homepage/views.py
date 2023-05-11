from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    ctx = {}
    if request.user:
        ctx['user'] = request.user
    return render(request, "index.html", ctx)