from django.contrib import admin
from django.urls import path
from . import views


app_name = 'user'

urlpatterns = [
    path("", views.index, name='index'),
    path("Codeshare/", views.home, name='codeshare'),
    path("NBcamp[-1]/", views.b_9, name='b_9'),
    path("signup/", views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('follows/', views.FollowList.as_view(), name='follow'),
    path('@<str:username>/follow/', views.add_or_sub_follower, name='following'),
    path('@<str:username>/update/', views.user_mypage_update, name='mypage-update'),
    path('@<str:username>/', views.user_mypage, name='mypage'),
    path('search/', views.UserList.as_view(), name='search'),

]
