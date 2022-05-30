from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('CreatePage', views.CreatePage,name='CreatePage'),
    path('UpdatePage', views.UpdatePage,name='UpdatePage'),
    path('DeletePage', views.DeletePage,name='DeletePage'),
    path('setConnectionString', views.setConnectionString,name='setConnectionString'),
    
]
