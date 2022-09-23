from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


@login_required
def home(request):
    # items = Items.objects.all()
    return render(request, 'index/index.html')


# def login_view(request):
#     return render(request, 'login.html')


def inicio_sesion(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
    else:
        # Return an 'invalid login' error message.
        ...


def logout_view(request):
    logout(request)
    return redirect('/')


def agregar_usuario_view(request):
    return render(request, 'agregar-usuario.html')


def libro_diario_view(request):
    return render(request, 'libro-diario.html')


def libro_mayor_view(request):
    return render(request, 'libro-mayor.html')


def plan_de_cuentas_view(request):
    return render(request, 'plan-de-cuentas.html')


def registrar_asiento_view(request):
    return render(request, 'registrar-asiento.html')
