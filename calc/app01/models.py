from django.db import models

# Create your models here.


class UserInfo(models.Model):
    username = models.CharField(max_length=32, default='')
    password = models.CharField(max_length=64, default='')


class ArticleInfo(models.Model):
    seed = models.CharField(max_length=100, default='')
    PostTime = models.CharField(max_length=100, default='')
    username = models.CharField(max_length=32, default='')
    title = models.CharField(max_length=200, default='')
    content = models.CharField(max_length=20000, default='')

