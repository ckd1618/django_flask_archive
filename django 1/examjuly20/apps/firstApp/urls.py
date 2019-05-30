from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('dashboard', views.dashboard),
    path('addjob', views.addjob),
    path('view/<int:num4>', views.viewnum),
    path('edit/<int:num5>', views.editnum),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('addjobsubmit', views.addjobsubmit),
    path('editjobsubmit/<int:num5>', views.editjobsubmit),
    path('cancel/<int:num6>', views.cancel),
    path('history', views.dashboard),
    path('addtomyjobs/<int:num7>', views.addtomyjobs),
]