from django.urls import path
from . import views 
urlpatterns = [
    path('', views.index),
    path('books', views.books),
    path('books/add', views.index),
    path('books/<int:num4>', views.index),
    path('users/<num5>', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
]