from django.shortcuts import render, redirect
# Create your views here.
def game(request):
    user = request.user
    if user.is_authenticated:
        return render(request, "play.html")
    else:
        return redirect('/login')
