from django.shortcuts import render
from .forms import *
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect

# Create your views here.
def page_logout(request):
    logout(request)
    return redirect('homepage')

class LoginView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return redirect('homepage')
        else:
            form = TestForm()
            ctx = {
                'form': form,
            }
            return render(request, "login.html", ctx)

    def post(self, request):
        form = TestForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('homepage')
            else:
                ctx = {
                    'form': form,
                    'msg': 'Wrong username or password.',
                }
            return render(request, "login.html", ctx)
        else:
            ctx = {
                'form': form,
                'msg': 'Wrong username or password.',
            }
            return render(request, "login.html", ctx)