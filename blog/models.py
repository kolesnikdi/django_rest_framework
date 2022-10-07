from django.conf import settings
from django.db import models
from django.utils import timezone

"""FOR DRF  --> Why we need this?"""
from pygments.lexers import get_all_lexers

LEXERS = [item for item in get_all_lexers() if item[1]]


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title