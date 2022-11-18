from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User', related_name='blogs', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    blog = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    published_date = models.DateTimeField(default=timezone.now)
