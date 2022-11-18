from rest_framework import serializers

from blog.models import Post, Comment


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')  # autofill author by the name of the author
    comments = serializers.PrimaryKeyRelatedField(many=True, queryset=Comment.objects.all())

    class Meta:
        model = Post
        fields = ['title', 'text', 'id', 'author', 'url', 'comments']


class SnippetSerializerPutPost(serializers.HyperlinkedModelSerializer):
    """"Another Serializer only for PutPost method fix problem with the possibility to change comment owner"""
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['title', 'text', 'id', 'author', 'url']


class CommentsSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['text', 'id', 'author']
