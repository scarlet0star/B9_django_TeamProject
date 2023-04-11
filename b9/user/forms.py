from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Profile


class UserCreateForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'last_name',
                  'first_name', 'password1', 'password2']


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['subscript','profile_image']

