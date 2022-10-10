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
    path('libro-diario', views.libro_diario_view, name='logout'),
    path('libro-mayor', views.libro_mayor_view, name='logout'),
    path('plan-de-cuentas', views.plan_de_cuentas_view, name='logout'),
    path('registrar-asiento', views.registrar_asiento_view, name='logout'),

    path('signup/', views.signup_view, name='signup'),
    # path('registrousuario', views.registro, name='registro'),
]
