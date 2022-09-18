from django.urls import path, include
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, logout_then_login
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('login', views.login, name='login'),
    # path('inicio', login, {'template_name': 'login.html'}, name='login'),
    path('logout', views.logout_view, name='logout')
]
