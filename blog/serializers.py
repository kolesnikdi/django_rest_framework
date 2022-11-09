from rest_framework import serializers

from blog.models import Post, Comment


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')  # autofill author by the name of the author
    comments = serializers.PrimaryKeyRelatedField(many=True, queryset=Comment.objects.all())  #todo Додає список коментарів і при публікації можна пиздить коменти собі під публікацію
    # comments = serializers.HyperlinkedRelatedField(view_name='comments', lookup_field='comments', many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['title', 'text', 'id', 'author', 'url', 'comments']
        # lookup_field = 'comments'
        # extra_kwargs = {
        #     'url': {'lookup_field': 'comments'}
        # }


class SnippetSerializerPutPost(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['title', 'text', 'id', 'author', 'url']



class CommentsSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    # url = serializers.HyperlinkedRelatedField(view_name='comments', lookup_field='url', many=True, read_only=True)
    #todo Зробити гіперлінк на пост

    class Meta:
        model = Comment
        fields = ['text', 'id', 'author']  # todo delete , 'url'
        # lookup_field = 'url'
        # extra_kwargs = {
        #     'url': {'lookup_field': 'url'}
        # }
