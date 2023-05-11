from django.shortcuts import render

# Create your views here.
def dev_logs(request):
    return render(request, "dev_logs.html")