from django.shortcuts import render
from .forms import *
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.
def page_logout(request):
    logout(request)
    return redirect('homepage')

class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('homepage')

        form = UserCreationForm()
        ctx = {
            'form': form,
        }
        return render(request, "register.html", ctx)

    def post(self, request):
        form = UserCreationForm(request.POST)
        ctx = {
            'form': form
        }
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(request, new_user)
            return redirect('homepage')

        return render(request, 'register.html', ctx)
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