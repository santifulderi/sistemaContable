from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


@login_required
def home(request):
    # items = Items.objects.all()
    return render(request, 'index/index.html')


def login(request):
    return render(request, 'login.html')


def inicio_sesion(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        ...


def logout_view(request):
    logout(request)
    return redirect('/')
