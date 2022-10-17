from django import forms

from blog.models import Post

"""
FOR DRF
"""
from rest_framework import serializers


# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ('title', 'text',)


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')  # was changed
    # text = serializers.HyperlinkedIdentityField(view_name='blog-text', format='html')  # was changed. Problem code/
    class Meta:
        model = Post
        fields = ['title', 'text', "id", 'author']