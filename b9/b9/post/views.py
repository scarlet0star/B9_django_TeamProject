from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PostModel, Comment, Like
from user.models import Profile, User
from .forms import PostForm
from django.http import HttpResponse

# Create your views here.

# 메인 페이지
def home(request):
    posts = PostModel.objects.all().order_by('-created_at')
    likes = Like.objects.all()
    return render (request, 'post/home.html', {'posts': posts, 'likes':likes})


# 글 작성 view
@login_required
def post_create(request):
    if request.method == 'GET':
        form = PostForm()
        return render(request, 'post/post_create.html',{'form': form})
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            user = request.user
            post = PostModel(
                writer = user,
                title = form.cleaned_data.get('title'),
                post = form.cleaned_data.get('post'),
                photo = form.changed_data.get('photo'),
            )
            post.save()
            return redirect('/post')

# 게시글 삭제
def post_delete(request, post_id):
    post = PostModel.objects.get(id=post_id)
    post.delete()
    return redirect('/post')

#댓글 추가
@login_required 
def add_comment(request,post_id):
    post = get_object_or_404(PostModel,pk=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        author = request.user 
        comment = Comment.objects.create(
            content=content,
            author=author,
            post=post
        )
        return redirect('post_detail', post_id=post.id)
    else:
        return redirect('post_list')


#게시물에 대한 좋아요를 토글하는 함수
@login_required
def toggle_like(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(PostModel, pk=post_id)
        user =request.user
        if post.like_users.filter(pk=user.pk).exists():
            post.like_users.remove(user)
            post.like_count -= 1
            post.save()
        else:
            post.like_users.add(user)
            post.like_count += 1
            post.save()
        return redirect('/post')
    return redirect('/user/login')


# #현재 사용자가 작성한 게시글에 대한 좋아요 알림을 보여주는 함수
# @login_required
# def like_notificatons(request):
#     likes = Like.objects.filter(post__writer=request.user).order_by('-created_at')
#     context = {'likes':likes}
#     return render(request, 'post/like_notifications.html', context)

def all_delete(request):
    PostModel.objects.all().delete()
    return redirect('/post')

