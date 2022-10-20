from django.urls import path, include
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, logout_then_login
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('login', views.login_view, name='login'),
    # path('inicio', login, {'template_name': 'login.html'}, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('agregar-usuario', views.registro, name='registro'),
    path('libro-diario', views.libro_diario_view, name='libro_diario'),
    path('libro-mayor', views.libro_mayor_view, name='libro_mayor'),
    path('plan-de-cuentas', views.plan_de_cuentas_view, name='plan_de_cuentas'),
    path('agregar-cuenta', views.agregar_cuenta_view, name='agregar_cuenta'),
    path('registrar-asiento', views.registrar_asiento_view, name='registrar_asiento'),

    path('registrar-nuevo-registro', views.registrar_asiento),
    path('is-valid-saldo', views.is_valid_saldo),
    path('get-nombre-cuenta', views.get_nombre_cuenta),

    # path('signup/', views.signup_view, name='signup'),
]
