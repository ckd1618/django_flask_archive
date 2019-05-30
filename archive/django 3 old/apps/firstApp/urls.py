from django.urls import path
from . import views 
urlpatterns = [
    path('', views.index),
    path('travels', views.travels),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('addtrip', views.addtrip),
    path('view/<int:num1>', views.viewnum),
    path('addjobr', views.addjobr),
    path('cancel/<int:num2>', views.cancelnum),
    path('join/<int:num3>', views.joinnum),
    path('delete/<int:num4>', views.deletenum),
]