from django.db import models
from django.contrib.auth.models import User
from user.models import User
from django.utils import timezone

# Create your models here.
class PostModel(models.Model):
    class Meta:
        db_table = "Post"

    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    post = models.TextField()
    photo = models.ImageField(blank=True, upload_to="media/%Y/%m/%d")
    like_users = models.ManyToManyField(User, related_name='like_articles')
    like_count = models.IntegerField(blank=True, null=True,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    contant = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    