from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.post_create, name='post_create'),
    path('<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('all-delete/', views.all_delete, name='all_delete'),
    # path('like_notifications/', views.like_notifications, name='like_notifications'),
]