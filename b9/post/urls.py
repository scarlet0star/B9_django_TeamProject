from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.post_create, name='post_create'),
    path('<int:id>/', views.detail_post, name='detail'),
    path('<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('<int:post_id>/', views.post_detail, name='detail_post'),
    path('<int:post_id>/comment/add/', views.add_comment, name='add_comment'),
    path('all-delete/', views.all_delete, name='all_delete'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    # path('like_notifications/', views.like_notifications, name='like_notifications'),
]
