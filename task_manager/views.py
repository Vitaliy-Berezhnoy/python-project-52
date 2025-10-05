from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


def test_error(request):
    # Это вызовет ошибку для тестирования Rollbar
    raise Exception("Test error for Rollbar")

def home(request):
    return render(request, "home.html")

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, _('You are logged in'))
            return redirect('home')
        else:
            messages.error(request, _('Please enter correct username and password'))

    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, _('You are logged out'))
    return redirect('home')