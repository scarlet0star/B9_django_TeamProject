from django.contrib import admin
from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static

app_name = 'user'

urlpatterns = [
    path("",views.index,name='index'),
    path("signup/", views.user_signup,name='signup'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('follows/',views.follow_list,name='follow'),
    path('follow/@<str:username>',views.add_or_sub_follower,name='following'),
    path('mypage/', views.user_mypage, name='mypage'),
    path('mypage/update', views.user_mypage_update, name='mypage-update'),

]
