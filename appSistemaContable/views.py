import ast
from contextlib import nullcontext
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
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


@login_required
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


@login_required
def agregar_usuario_view(request):
    return render(request, 'agregar-usuario.html')


@login_required
def libro_diario_view(request):
    asientos = Asiento.objects.all().order_by('fecha')
    cuenta_asiento = CuentaAsiento.objects.all()
    # cuentas = Cuentas.objects.all()
    cuentas = Cuentas.objects.filter(recibe_saldo=True)
    return render(request, 'libro-diario.html',
                  {'asientos': asientos, 'cuenta_asiento': cuenta_asiento, 'cuentas': cuentas, 'query': nullcontext})


@login_required
def libro_mayor_view(request):
    cuentas = Cuentas.objects.filter(recibe_saldo=True).order_by('codigo')
    return render(request, 'libro-mayor.html',
                  {'cuentas': cuentas, 'query': nullcontext})


@login_required
def get_cuenta_asientos(request):
    result = ast.literal_eval(request.body.decode('utf-8'))
    id_cuenta = result['id_cuenta']
    cuenta_asientos = CuentaAsiento.objects.filter(id_cuenta=id_cuenta)
    # print("Query entera de todos los renglones asociados a la cuenta: ", cuenta_asientos.values())
    resultado = []

    # Caso de que con el id se haya encontrado la cuenta_asiento
    if len(cuenta_asientos) > 0:
        for x in cuenta_asientos:
            print("XXXXXXXXXXXXXXX ", x)
            print("XXXXXXXXXXXXXXX ", x.id_cuenta.id)
            print("iddddddddddddddddd ", x.id_asiento.id)
            aux = []
            asiento_asociado = Asiento.objects.filter(id=x.id_asiento.id)[0]
            print("Asiento asociadooooooooooo ", asiento_asociado)
            aux.append(asiento_asociado.fecha)
            aux.append(asiento_asociado.descripcion)
            aux.append(x.debe)
            aux.append(x.haber)
            aux.append(x.saldo) #por ahi se quita
            resultado.append(aux)
            print(aux)
            print(resultado)
        data = {
            'cuenta_asientos': resultado,
            'mensaje': "Exito..."
        }
    else:
        data = {
            'mensaje': "Error..."
        }
    return JsonResponse(data)


@login_required
def plan_de_cuentas_view(request):
    cuentas = Cuentas.objects.all().order_by('codigo')
    return render(request, 'plan-de-cuentas.html', {'cuentas': cuentas, 'query': nullcontext})


@login_required
def existe_codigo_cuenta(request):
    print("Llega a la funcion de existe_codigo_cuenta")
    result = ast.literal_eval(request.body.decode('utf-8'))
    codigo = result['codigo']
    existe = False

    # value = Cuentas.objects.filter(codigo=codigo)
    value = Cuentas.objects.all()

    for x in value:
        if x.codigo == codigo:
            existe = True
            break

    if len(value) > 0:
        data = {
            'existe': existe,
            'mensaje': "Ya existe una cuenta con dicho código"
        }
    else:
        data = {
            'existe': existe,
            'mensaje': "No existe una cuenta con dicho código"
        }
    print("El código existe: ", existe)
    return JsonResponse(data)


@login_required
def registrar_cuenta(request):
    print("Llega a registrar_cuenta")
    result = ast.literal_eval(request.body.decode('utf-8'))
    nombre = result['nombre']
    codigo = result['codigo']
    tipo = result['tipo']
    recibe_saldo = result['recibe_saldo']
    saldo = result['saldo']

    if recibe_saldo>0:
        new_cuenta = Cuentas.objects.create(cuenta=nombre, codigo=codigo, tipo=tipo, recibe_saldo=True,
                                            saldo_actual=saldo)
    else:
        new_cuenta = Cuentas.objects.create(cuenta=nombre, codigo=codigo, tipo=tipo, recibe_saldo=False)

    data = {
        'mensaje': "Cuenta registrada"
    }
    return JsonResponse(data)


@login_required
def agregar_cuenta_view(request):
    cuentas = Cuentas.objects.all().order_by('codigo')
    return render(request, 'AUX.html', {'cuentas': cuentas, 'query': nullcontext})


@login_required
def is_valid_saldo(request):
    result = ast.literal_eval(request.body.decode('utf-8'))
    id_cuenta = result['id_cuenta']
    monto = result['monto']
    monto = float(monto)
    tipo_operacion = result['tipo_operacion']

    value = Cuentas.objects.filter(id=id_cuenta)
    print(value[0].tipo)

    # Caso de que con el id se haya encontrado la cuenta
    if len(value) > 0:
        if tipo_operacion == 'debe':
            if value[0].tipo == 'AC':
                # la cuenta es de activo y va por el debe
                data = {
                    'value': True,
                    'mensaje': "Comprobación realizada en el saldo de la cuenta, saldo mayor a 0"
                }
            elif value[0].tipo == 'PA' or value[0].tipo == 'PM':
                # la cuenta es de pasivo y va por el debe
                # o
                # la cuenta es de patrimonio y va por el debe
                if (float(value[0].saldo_actual) - monto) >= 0:
                    data = {
                        'value': True,
                        'mensaje': "Comprobación realizada en el saldo de la cuenta, saldo mayor a 0"
                    }
                else:
                    data = {
                        'value': False,
                        'mensaje': "Comprobación realizada en el saldo de la cuenta, saldo menor a 0"
                    }
            # elif value[0].tipo == 'PM':
            #     pass
            #     # la cuenta es de patrimonio y va por el debe
            elif value[0].tipo == 'R-':
                # la cuenta es de resultado + y va por el debe
                data = {
                    'value': True,
                    'mensaje': "Comprobación realizada en el saldo de la cuenta, saldo mayor a 0"
                }
            elif value[0].tipo == 'R+':
                # la cuenta es de resultado - y va por el debe
                data = {
                    'value': False,
                    'mensaje': "La cuenta es de Positivo(R+), se registra por el haber"
                }

        else:  # tipo_operacion == 'haber'
            if value[0].tipo == 'AC':
                # la cuenta es de activo y va por el haber
                if (float(value[0].saldo_actual) - monto) >= 0:
                    data = {
                        'value': True,
                        'mensaje': "Comprobación realizada en el saldo de la cuenta, saldo mayor a 0"
                    }
                else:
                    data = {
                        'value': False,
                        'mensaje': "Comprobación realizada en el saldo de la cuenta, saldo menor a 0"
                    }
            elif value[0].tipo == 'PA' or value[0].tipo == 'PM':
                # la cuenta es de pasivo y va por el haber
                # o
                # la cuenta es de patrimonio y va por el haber
                data = {
                    'value': True,
                    'mensaje': "Comprobación realizada en el saldo de la cuenta, saldo mayor a 0"
                }
            # elif value[0].tipo == 'PM':
            #     pass
            #     # la cuenta es de patrimonio y va por el haber
            elif value[0].tipo == 'R-':
                # la cuenta es de resultado + y va por el haber
                data = {
                    'value': False,
                    'mensaje': "La cuenta es de Resultado Resultado Negativo(R-), se registra por el debe"
                }
            elif value[0].tipo == 'R+':
                # la cuenta es de resultado - y va por el haber
                data = {
                    'value': True,
                    'mensaje': "Comprobación realizada en el saldo de la cuenta, saldo mayor a 0"
                }

    else:
        # Caso de que con el id NO se haya encontrado la cuenta
        data = {
            'mensaje': "Error del sistema, cuenta no encontrada"
        }
        print("No fue posible realizar la comprobación")
    return JsonResponse(data)


@login_required
def registrar_asiento_view(request):
    asientos = Asiento.objects.all()
    num_prox_asiento = len(asientos) + 1
    # cuentas = Cuentas.objects.all()
    cuentas = Cuentas.objects.filter(recibe_saldo=True).order_by('codigo')
    print("Tipo de dato:", type(cuentas))
    return render(request, 'registrar-asiento.html',
                  {'asientos': asientos, 'num_prox_asiento': num_prox_asiento, 'cuentas': cuentas,
                   'query': nullcontext})


def get_id_user(request):
    current_user = request.user
    print(current_user.id)
    return current_user.id


def get_nombre_cuenta(request):
    result = ast.literal_eval(request.body.decode('utf-8'))
    id_cuenta = result['id_cuenta']
    cuenta = Cuentas.objects.filter(id=id_cuenta)[0]
    print(Cuentas.objects.filter(id=id_cuenta)[0])
    nombre_cuenta = cuenta.cuenta
    print(nombre_cuenta)
    data = {
        'nombre': nombre_cuenta
    }
    return JsonResponse(data)


def get_cuenta_by_id(id):
    return Cuentas.objects.filter(id=id)[0]


@login_required
def registrar_asiento(request):
    print(request)
    user = request.user
    result = ast.literal_eval(request.body.decode('utf-8'))
    descripcion = result['descripcion']
    array_renglones = result['array_renglones']

    new_asiento = Asiento.objects.create(descripcion=descripcion, id_usuario=user)

    for renglon in array_renglones:
        cuenta = get_cuenta_by_id(renglon[0])
        debe_decimal = Decimal(renglon[1])
        haber_decimal = Decimal(renglon[2])
        if cuenta.tipo == 'AC':
            print("Saldo actual de la cuenta ", cuenta.cuenta, ": ", cuenta.saldo_actual)
            cuenta.saldo_actual += debe_decimal
            cuenta.saldo_actual -= haber_decimal
            print("Saldo actual de la cuenta ", cuenta.cuenta, "(actualizado): ", cuenta.saldo_actual)
        if cuenta.tipo == 'PA':
            cuenta.saldo_actual += haber_decimal
            cuenta.saldo_actual -= debe_decimal
        if cuenta.tipo == 'R+':
            cuenta.saldo_actual += debe_decimal
        if cuenta.tipo == 'R-':
            cuenta.saldo_actual -= haber_decimal
        if cuenta.tipo == 'PM':
            cuenta.saldo_actual += haber_decimal
            cuenta.saldo_actual -= debe_decimal
        cuenta.save()
        new_renglon = CuentaAsiento.objects.create(id_cuenta=cuenta, id_asiento=new_asiento, debe=renglon[1],
                                                   haber=renglon[2], saldo=renglon[3])

    data = {
        'mensaje': "Error del sistema, cuenta no encontrada"
    }
    return JsonResponse(data)


@login_required
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
