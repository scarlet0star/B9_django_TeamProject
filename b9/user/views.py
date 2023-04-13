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
# Create your views here.


def index(request):
    return render(request, "user/index.html")


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
    # likes = Like.objects.filter(user=username)
    return render(request, 'user/mypage.html', {'profile': profile, 'posts': all_mypost, })


@login_required
def user_mypage_update(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        profileform = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile)

        if form.is_valid() and profileform.is_valid():
            form.save()
            profileform.save()
            messages.success(request, '프로필이 업데이트 되었습니다!')
            return redirect('/user/mypage')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'user/mypage_update.html', {'form': user_form, 'profileform': profile_form})


@login_required
def follow_list(request):
    follows = request.user.profile.follows.all()
    return render(request, 'user/follow_list.html', {'follows': follows})


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
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', '')
        context['search_by'] = self.request.GET.get('search_by', 'ID')
        return context
