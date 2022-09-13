from django.urls import path

from . import views
# from .views import ItemView, ItemAugmentedView, AddLike
# from django.contrib.auth.views import logout_then_login

urlpatterns = [
    path('', views.home, name='home'),
]