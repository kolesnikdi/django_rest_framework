from django import forms

from blog.models import Post

"""
FOR DRF
"""
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)


"""
FOR DRF
"""


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'text',]