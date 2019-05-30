from django.urls import path
from . import  views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('logout', views.logout),
    path('gamble', views.gamble),
    path('score/<int:player_id>', views.show_player),
    path('edit', views.edit),
    path('update', views.update),
    path('follow/<int:player_id>', views.follow),
]
