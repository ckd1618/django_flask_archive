from django.urls import path
from . import views 
urlpatterns = [
    path('', views.index),
    path('quotes', views.quotes),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('addnewquote', views.addnewquote),
    path('addlike/<int:num1>', views.addlike),
    path('user/<int:num2>', views.usernum),
    path('myaccount', views.myaccountnum),
    path('x', views.myaccountform),
    path('cancel/<int:num6>', views.cancel),
    path('valquote', views.valquote),
]