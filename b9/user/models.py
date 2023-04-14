from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(
        "ID", max_length=24, unique=True, primary_key=True,)

    def __str__(self):
        return f'{self.username} : {self.last_name}{self.first_name}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscript = models.CharField("유저소개문(짧게)", max_length=200, blank=True)
    profile_image = models.ImageField("유저이미지", upload_to='profile_images/', blank=True, null=True)
    follows = models.ManyToManyField(
        'self', through='Follow', related_name='follwers', symmetrical=False)
    
    def __str__(self):
        return f'{self.user.username}'


class Follow(models.Model):
    follower = models.ForeignKey(
        Profile, related_name="following", on_delete=models.CASCADE)
    followee = models.ForeignKey(
        Profile, related_name="followed_by", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.follower} 팔로우-> {self.followee}'
    
    def is_following(self, target_profile):
        return self.following.filter(followee=target_profile).exists()

