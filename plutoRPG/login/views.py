from django.shortcuts import render
from .forms import *
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm

def page_logout(request):
    """
    Logging the user out.

    :param request: Django request object.
    :return: (HttpResponse) Redirect to homepage.
    """
    logout(request)
    return redirect('homepage')
class RegisterView(View):
    """Handles request to register user."""
    def get(self, request):
        """
        Handles request to register user, authentication stage.

        :param request: Django request object.
        :return: (HttpResponse) Redirect to homepage or register page.
        """
        if request.user.is_authenticated:
            return redirect('homepage')

        form = UserCreationForm()
        ctx = {
            'form': form,
        }
        return render(request, "register.html", ctx)
    def post(self, request):
        """
        Handles request to register user based on form data, creation stage.

        :param request: Django request object.
        :return: (HttpResponse) Redirect to homepage or register page.
        """
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
    """ Handles request to log user in """
    def get(self, request):
        """
        Handles request to log user in, authentication stage #1.

        :param request: Django request object.
        :return: (HttpResponse) Redirect to homepage or login page.
        """
        user = request.user
        if user.is_authenticated:
            return redirect('homepage')
        else:
            form = LoginForm()
            ctx = {
                'content': 'page_login',
                'form': form,
            }
            return render(request, "login.html", ctx)

    def post(self, request):
        """
        Handles request to log user in, authentication stage #2.

        :param request: Django request object.
        :return: (HttpResponse) Redirect to homepage or login page.
        """
        form = LoginForm(request.POST)
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