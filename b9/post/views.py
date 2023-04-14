from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from user.models import Profile, User
from .forms import PostForm, CommentForm
from django.http import HttpResponse
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.views.generic import ListView, TemplateView
from django.db.models import Q
# Create your views here.

# 메인 페이지


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
    return render(request, 'post/post_create.html', {'form': form})


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


class UpdatePost(UpdateView):
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'id'
    template_name = 'post/post_create.html'

    def get_success_url(self):
        return reverse_lazy('post:detail', kwargs={'id': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        return context


# sdfsdf
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        print('post')
        form = CommentForm(request.POST)
        if form.is_valid():
            print('ok')
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post:detail_post', post_id)
    return redirect('post:detail_post', post_id)


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return redirect('post:detail_post', comment.post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post:detail_post', comment.post_id)
    else:
        form = CommentForm(instance=comment)
    return redirect('post:detail_post',  comment.post_id)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    print(comment.post_id)
    if comment.author != request.user:
        return redirect('post:detail_post', comment.post_id)
    comment.delete()
    return redirect('post:detail_post', comment.post_id)


@login_required
def toggle_like(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=post_id)
        user = request.user
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
def detail_post(request, post_id):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            post_detail = Post.objects.get(id=post_id)
            # all_comment = Comment.
            commentform = CommentForm()
            all_comment = Comment.objects.filter(post_id=post_id)
            return render(request, 'post/detail.html', {'post_detail': post_detail, 'all_comment': all_comment, 'commentform': commentform})
        else:
            return redirect('login')
    if request.method == 'DELETE':
        post = Post.objects.get(id=post_id)
        post.delete()
        return redirect('/post')

# 페이지 검색 기능
def search(request):
    searched = request.GET.get('postsearched', '')
    posts = Post.objects.filter(Q(title__icontains=searched)|
                                Q(post__icontains=searched)
                                ).distinct().order_by('-created_at')
    return render(request, 'post/post_searched.html', {'searched':searched,'posts_searched':posts})

class PostList(ListView):
    model = Post
    template_name = 'post/post_searched.html'
    context_object_name = 'posts_searched'
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        if query:
            return self.model.objects.filter(Q(title__icontains=query)|
                                Q(post__icontains=query)
                                ).distinct().order_by('-created_at')
        else:
            return self.model.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', '')
        return context
