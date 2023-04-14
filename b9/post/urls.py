from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('create/', views.post_create, name='post_create'),
    path('<int:id>/update/', views.UpdatePost.as_view(), name='post_update'),
    path('<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('<int:post_id>/', views.detail_post, name='detail_post'),
    path('<int:post_id>/comment/add/', views.add_comment, name='add_comment'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('tag/', views.TagCloudTV.as_view(), name='tag_cloud'),
    # 태그 내 문자열로 들어가면
    path('tag/<str:tag>/', views.TaggedObjectLV.as_view(), name='tagged_object_list'),
    # 페이지 검색 기능
    path('search/',views.PostList.as_view(), name='post_searched')
    # path('like_notifications/', views.like_notifications, name='like_notifications'),
]
