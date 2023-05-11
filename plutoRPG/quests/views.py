from django.shortcuts import render

# Create your views here.
def quests(request):
    return render(request, "quests.html")