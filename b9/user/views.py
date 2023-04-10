from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.


def index(request):
    return render(request, "user/user.html")


def user_signup(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user:login')
        else:
            messages.error(request, form.errors)
            messages.error(request, form.non_field_errors())

    else:
        form = UserCreateForm()
    return render(request, 'user/signup.html', {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "user is None")
        else:   
            messages.error(request, "form is not valid")
            print("Form Errors: ", form.errors)
            print("Non-field Errors: ", form.non_field_errors())
    else:
        form = AuthenticationForm(request)
    return render(request, 'user/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def follow_list(request):
    follows = request.user.Profile.follows.all()
    return render(request,'user/follow_list.html',{'follows':follows})

@login_required
def add_or_sub_follower(request,uid):
    target = get_object_or_404('Profile',pk=uid)
    user_profile = request.user.Profile
    
    if user_profile.follows.filter(id=target.id).exist():
        user_profile.follows.remove(target)
    else:
        user_profile.follows.add(target)

    return 