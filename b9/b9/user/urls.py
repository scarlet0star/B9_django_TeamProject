from django.contrib import admin
from django.urls import path
from . import views 

app_name = 'user'

urlpatterns = [
    path("",views.index,name='index'),
    path("signup/", views.user_signup,name='signup'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('profile/',views.user_logout,name='profile'),
]
