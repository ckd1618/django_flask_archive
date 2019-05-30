from django.urls import path
from . import views 
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('wall', views.wall),
    path('message', views.message),
    path('comment/<int:message_id>', views.comment),
    path('user/<int:user_id>', views.show)
]
