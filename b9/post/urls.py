from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.post_create, name='post_create'),
    path('<int:id>/', views.detail_post, name='detail'),
    path('<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('tag/', views.TagCloudTV.as_view(), name='tag_cloud'),
    # 태그 내 문자열로 들어가면
    path('tag/<str:tag>/', views.TaggedObjectLV.as_view(), name='tagged_object_list'),
    # path('like_notifications/', views.like_notifications, name='like_notifications'),
]
