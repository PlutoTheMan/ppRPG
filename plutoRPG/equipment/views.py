from django.shortcuts import render

# Create your views here.
def equipment(request):
    return render(request, "equipment.html")