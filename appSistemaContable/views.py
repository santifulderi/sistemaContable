from contextlib import nullcontext

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .models import *
from .forms import CustomUserCreationForm

from .forms import UserLoginForm, UserSignUpForm

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
    cuentas = Cuentas.objects.all()
    return render(request, 'plan-de-cuentas.html', {'cuentas': cuentas, 'query': nullcontext})


def registrar_asiento_view(request):
    return render(request, 'registrar-asiento.html')


def signup_view(request):
    signup_form = UserSignUpForm(request.POST or None)
    if signup_form.is_valid():
        email = signup_form.cleaned_data.get('email')
        name = signup_form.cleaned_data.get('name')
        password = signup_form.cleaned_data.get('password')
        mobile = signup_form.cleaned_data.get('mobile')

        user = get_user_model().objects.create(
            email=email,
            name=name,
            password=make_password(password),
            mobile=mobile,
            is_active=True
        )
        login(request, user)
        return redirect('home')

    else:
        return redirect('home')


def registro(request):
    data = {
        'form': CustomUserCreationForm
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect(to='home')
        data["form"] = formulario

    return render(request, 'agregar-usuario.html', data)