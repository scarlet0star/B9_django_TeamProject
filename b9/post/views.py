from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.contrib.auth import get_user_model
from .forms import PostForm
from django.core.paginator import Paginator
from django.views.generic import ListView, TemplateView
from django.http import HttpResponse
# Create your views here.

# 메인 페이지
def home(request):
    post_list = Post.objects.all().order_by('-created_at')
    # 포스트리스트를 5개씩 나누기
    paginator = Paginator(post_list, 5)
    # 페이지에 해당되는 페이지의 번호를 받아오기
    page = request.GET.get('page')
    # 페이지 번호를 받아서 해당 페이지 게시글들을 리턴하기
    posts = paginator.get_page(page)
    # 받아온 페이지를 render를 통해 넘겨주기
    return render (request, 'post/home.html', {'posts': posts})

# 글 작성 view
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        user = request.user
        tags = request.POST.get('tags', '').split(',')
        if form.is_valid():
            post = Post.objects.create(
                writer=user,
                title=form.cleaned_data.get('title'),
                post=form.cleaned_data.get('post'),
                photo=form.cleaned_data.get('photo'),
            )
            for tag in tags:
                tag = tag.strip()
                if tag != '':
                    post.tags.add(tag)
            post.save()
            return redirect('/post')
    if request.method == 'GET':
        form = PostForm()
    return render(request, 'post/post_create.html',{'form': form})

class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'

# 태그가 있으면 태그를 보여주겠다.
class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context

#댓글 추가
@login_required 
def add_comment(request,post_id):
    post = get_object_or_404(Post,pk=post_id)
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