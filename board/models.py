from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class School(models.Model):
    school = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)


class Board(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=False, blank=False)
    board = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False, related_name='comments')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
