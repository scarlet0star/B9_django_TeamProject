from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from taggit.managers import TaggableManager

# Create your models here.
class Post(models.Model):
    class Meta:
        db_table = "Post"

    writer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    post = models.TextField()
    photo = models.ImageField("포스트이미지",upload_to="post_photo/%Y/%m/%d" , blank=True, null=True)
    like_users = models.ManyToManyField(get_user_model(), related_name='like_articles')
    like_count = models.IntegerField(blank=True, null=True,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager(blank=True)
    

class Comment(models.Model):
    content = models.TextField("댓글 작성")
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content



    