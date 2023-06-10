from django.shortcuts import render

# Create your views here.
def quests(request):
    """
    Rendering quests page.
    :param request: Django request object.
    :return: (HttpResponse) quests page.
    """
    return render(request, "quests.html", {'content': 'quests'})