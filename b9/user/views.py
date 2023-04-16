from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import *
from .models import Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from post.models import Post
from django.views.generic import ListView
from django.db.models import Q
from django.core.paginator import Paginator


def b_9(request):
    return render(request, "NBcamp[-1].html")


# Create your views here.
def home(request):
    return render(request, "Codeshare.html")


def index(request):
    post_list = Post.objects.all().order_by('-created_at')
    # 포스트리스트를 5개씩 나누기
    paginator = Paginator(post_list, 4)
    # 페이지에 해당되는 페이지의 번호를 받아오기
    page = request.GET.get('page')
    # 페이지 번호를 받아서 해당 페이지 게시글들을 리턴하기
    posts = paginator.get_page(page)

    # FollowerPostList의 로직을 추가
    user = request.user
    if user.is_authenticated:
        following_users = user.profile.follows.all()
        if following_users:
            following_ids = [u.user.pk for u in following_users]
            followings = Post.objects.filter(writer__in=following_ids)
        else:
            followings = Post.objects.none()
    else:
        followings = None
    context = {
        'posts': posts,
        'followings': followings.order_by('-created_at') if followings else None
    }

    return render(request, "user/index.html", context)


def user_signup(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('user:login')
        else:
            messages.error(request, form.errors)
            messages.error(request, form.non_field_errors())

    else:
        form = UserCreateForm()
    return render(request, 'user/signup.html', {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user:index')
            else:
                messages.error(request, "user is None")
        else:
            messages.error(request, "form is not valid")
            print("Form Errors: ", form.errors)
            print("Non-field Errors: ", form.non_field_errors())
    else:
        form = AuthenticationForm(request)
    return render(request, 'user/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('user:login')


@login_required
def user_mypage(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    profile = Profile.objects.get(user=user)
    all_mypost = Post.objects.filter(writer=username).order_by('-created_at')

    if request.user.username == username:
        # 현재 로그인한 사용자와 페이지 주인이 같은 경우
        user_profile = profile
        is_following = None
    else:
        # 다른 사용자의 페이지인 경우 해당 사용자의 프로필 정보를 전달
        user_profile = Profile.objects.get(user=user)
        is_following = request.user.profile.is_following(profile)

    print(is_following)

    return render(request, 'user/mypage.html', {'profile': profile, 'posts': all_mypost, 'user_profile': user_profile, 'is_following': is_following})


@login_required
def user_mypage_update(request, username):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        profileform = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile)

        if form.is_valid() and profileform.is_valid():
            form.save()
            profileform.save()
            messages.success(request, '프로필이 업데이트 되었습니다!')
            return redirect('user:mypage', username=username)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'user/mypage_update.html', {'form': user_form, 'profileform': profile_form})


@login_required
def add_or_sub_follower(request, username):
    target = get_object_or_404(get_user_model(), username=username)
    target_profile = target.profile
    user_profile = request.user.profile

    if user_profile.follows.filter(id=target_profile.id).exists():
        user_profile.follows.remove(target_profile)
    else:
        user_profile.follows.add(target_profile)

    return redirect('user:index')


class UserList(ListView):
    model = get_user_model()
    template_name = 'user/user_list.html'
    context_object_name = 'users'
    paginate_by = 3

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return self.model.objects.none()

        query = self.request.GET.get('query', '')
        search_by = self.request.GET.get('search_by', 'ID')

        if query:
            if search_by == 'ID':
                return self.model.objects.filter(username__icontains=query)
            elif search_by == 'first_name':
                return self.model.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
            else:
                return self.model.objects.none()

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            return self.model.objects.none()

        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', '')
        context['search_by'] = self.request.GET.get('search_by', 'ID')

        return context


class FollowList(ListView):
    model = get_user_model()
    template_name = 'user/user_list.html'
    context_object_name = 'users'
    paginate_by = 3

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return self.model.objects.none()

        follows = self.request.user.profile.follows.all()
        usernames = [profile.user.username for profile in follows]
        return self.model.objects.filter(username__in=usernames)
