from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Like
from user.models import Profile, User
from .forms import PostForm, CommentForm

from django.http import HttpResponse
# Create your views here.

# 메인 페이지
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    likes = Like.objects.all()
    return render (request, 'post/home.html', {'posts': posts, 'likes':likes})

# 글 작성 view
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        user = request.user
        if form.is_valid():
            post = Post(
                writer = user,
                title = form.cleaned_data.get('title'),
                post = form.cleaned_data.get('post'),
                photo = form.cleaned_data.get('photo'),
            )
            post.save()
            return redirect('/post')
    if request.method == 'GET':
        form = PostForm()
    return render(request, 'post/post_create.html',{'form': form})


#게시물에 대한 좋아요를 토글하는 함수
@login_required
def toggle_like(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=post_id)
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
    Post.objects.all().delete()
    return redirect('/post')

@login_required
def detail_post(request, id):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            post_detail = Post.objects.get(id=id)
            # all_comment = Comment.
            return render(request, 'post/detail.html', {'post_detail': post_detail})
        else:
            return redirect('login')
    if request.method == 'DELETE':
        post = Post.objects.get(id=id)
        post.delete()
        return redirect('/post')

## sdfsdf
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = CommentForm()
    return render(request, 'post/detail.html', {'form': form})

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return redirect('post_detail', post_id=comment.post.id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'post/detail.html', {'form': form})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return redirect('post_detail', post_id=comment.post.id)
    comment.delete()
    return redirect('post_detail', post_id=comment.post.id)