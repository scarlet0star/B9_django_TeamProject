from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField("ID",max_length=24, unique=True, primary_key=True,)
    def __str__(self):
        return f'{self.username} : {self.first_name}{self.last_name}'

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    subscript = models.CharField("유저소개문(짧게)",max_length=200)
    profile_image = models.ImageField("유저이미지")