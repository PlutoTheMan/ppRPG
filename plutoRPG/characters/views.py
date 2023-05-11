from django.shortcuts import render, redirect

# Create your views here.
def character_manager(request):
    if request.user.is_authenticated:
        return render(request, "character_manager.html")
    else:
        return redirect('homepage')