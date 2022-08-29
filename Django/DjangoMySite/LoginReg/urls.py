from django.urls import path
# Author - Kiran K. Mungekar.
from . import views

urlpatterns = [
    path('',views.loginReg,name='loginReg'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
]

