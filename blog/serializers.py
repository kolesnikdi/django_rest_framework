from rest_framework import serializers

from blog.models import Post


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['title', 'text', "id", 'author']