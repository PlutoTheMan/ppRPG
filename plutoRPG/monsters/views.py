from django.shortcuts import render

# Create your views here.
def monsters(request):
    return render(request, "monsters.html")
